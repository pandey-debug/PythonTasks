import os
import random
import string
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import pymysql
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ─────────────────────────────────────────────────────────────────────────────
# 🛠️ DATABASE SETUP (NATIVE MYSQL WITH COLD-START FAILSAFE)
# ─────────────────────────────────────────────────────────────────────────────
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME", "cinebook_db")

try:
    # Proactively check / create backend database schema on the MySQL host
    temp_conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=int(DB_PORT)
    )
    cursor = temp_conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    temp_conn.commit()
    cursor.close()
    temp_conn.close()
    
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(DATABASE_URL)
    print("Database Core successfully connected via native MySQL engine.")
except Exception as mysql_err:
    print(f"MySQL Connection Warning: {mysql_err}")
    print("Falling back to local SQLite engine (movie_booking.db) for playground compatibility...")
    DATABASE_URL = "sqlite:///./movie_booking.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ─────────────────────────────────────────────────────────────────────────────
# 🗄️ SQLALCHEMY MODELS
# ─────────────────────────────────────────────────────────────────────────────
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, index=True, nullable=False)
    phone = Column(String(50), nullable=False)
    role = Column(String(50), default="user", nullable=False)
    password = Column(String(255), nullable=False)

class MovieModel(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    genre = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes
    rating = Column(String(50), nullable=False)  # e.g., "PG-13", "R"
    image_url = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    total_seats = Column(Integer, default=50)
    available_seats = Column(Integer, default=50)
    show_date = Column(String(50), nullable=False)
    show_time = Column(String(50), nullable=False)
    theater_name = Column(String(255), nullable=True)
    slot = Column(String(100), nullable=True)
    status = Column(String(50), default="active")  # "active" or "completed"


class CompletedMovieModel(Base):
    __tablename__ = "completed_movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    genre = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    rating = Column(String(50), nullable=False)
    image_url = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    total_seats = Column(Integer, default=50)
    available_seats = Column(Integer, default=50)
    show_date = Column(String(50), nullable=False)
    show_time = Column(String(50), nullable=False)
    theater_name = Column(String(255), nullable=True)
    slot = Column(String(100), nullable=True)
    status = Column(String(50), default="completed")


class BookingModel(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    seats_booked = Column(Integer, nullable=False)
    booking_date = Column(String(50), nullable=False)
    booking_time = Column(String(50), nullable=False)
    booking_reference = Column(String(50), unique=True, index=True, nullable=False)


Base.metadata.create_all(bind=engine)


# ─────────────────────────────────────────────────────────────────────────────
# 📝 PYDANTIC SCHEMAS
# ─────────────────────────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    role: Optional[str] = "user"
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    role: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    name:     str
    password: str

class LoginResponse(BaseModel):
    id:       int
    name:     str
    role:     str

class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    genre: str
    duration: int
    rating: str
    image_url: Optional[str] = None
    price: float
    total_seats: int = 50
    available_seats: Optional[int] = None
    show_date: str
    show_time: str
    theater_name: Optional[str] = None
    slot: Optional[str] = None


class MovieResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    genre: str
    duration: int
    rating: str
    image_url: Optional[str]
    price: float
    total_seats: int
    available_seats: int
    show_date: str
    show_time: str
    theater_name: Optional[str]
    slot: Optional[str]
    status: str

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    user_id: int
    movie_id: int
    seats_booked: int
    booking_date: str
    booking_time: str


class BookingResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    seats_booked: int
    booking_date: str
    booking_time: str
    booking_reference: str

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# 🚀 FASTAPI APP INITIALIZATION
# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(title="Movie Ticketing System Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_booking_ref() -> str:
    letters = "".join(random.choices(string.ascii_uppercase, k=3))
    digits = "".join(random.choices(string.digits, k=4))
    return f"BK-{letters}{digits}"


# ─────────────────────────────────────────────────────────────────────────────
# Seed Initial Movies if Database is Empty
# ─────────────────────────────────────────────────────────────────────────────
def seed_database():
    db = SessionLocal()
    try:
        # Create an admin user if not exists
        if db.query(UserModel).filter(UserModel.name == "admin").count() == 0:
            db.add(UserModel(name="admin", phone="+919999999999", role="admin", password=pwd_context.hash("admin123")))
            db.commit()

        if db.query(MovieModel).count() == 0:
            sample_movies = [
                {
                    "title": "Interstellar Odyssey",
                    "description": "A group of astronauts travel through a wormhole in search of a new home for humanity amidst a collapsing biosphere.",
                    "genre": "Sci-Fi / Adventure",
                    "duration": 169,
                    "rating": "PG-13",
                    "image_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&auto=format&fit=crop&q=80",
                    "price": 14.99,
                    "total_seats": 60,
                    "available_seats": 60,
                    "show_date": "2026-06-01",
                    "show_time": "19:30",
                    "theater_name": "Titan IMAX Theater",
                    "slot": "Evening Block (19:30)",
                    "status": "active"
                },
                {
                    "title": "Cyberpunk 2099",
                    "description": "In a neon-drenched metropolis, a cybernetic mercenary attempts to bring down an all-powerful AI mega-corporation.",
                    "genre": "Sci-Fi / Action",
                    "duration": 142,
                    "rating": "R",
                    "image_url": "https://images.unsplash.com/photo-1578894381163-e72c17f2d45f?w=600&auto=format&fit=crop&q=80",
                    "price": 12.50,
                    "total_seats": 40,
                    "available_seats": 38,
                    "show_date": "2026-06-02",
                    "show_time": "21:00",
                    "theater_name": "Neo Lounge Screen 3",
                    "slot": "Late Night Block (21:00)",
                    "status": "active"
                },
                {
                    "title": "The Whispering Woods",
                    "description": "An enchanted fantasy tale of a young healer who enters a forbidden, sentient forest to cure a mystical plague.",
                    "genre": "Fantasy / Animation",
                    "duration": 115,
                    "rating": "PG",
                    "image_url": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=600&auto=format&fit=crop&q=80",
                    "price": 11.00,
                    "total_seats": 50,
                    "available_seats": 50,
                    "show_date": "2026-06-03",
                    "show_time": "14:00",
                    "theater_name": "Kids Dream Hall A",
                    "slot": "Matinee Block (14:00)",
                    "status": "active"
                },
                {
                    "title": "Chef's Special Choice",
                    "description": "A heartwarming comedy drama about a high-class chef who loses his restaurant and starts a humble mobile food truck.",
                    "genre": "Comedy / Drama",
                    "duration": 133,
                    "rating": "PG-13",
                    "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&auto=format&fit=crop&q=80",
                    "price": 10.00,
                    "total_seats": 30,
                    "available_seats": 25,
                    "show_date": "2026-06-04",
                    "show_time": "17:45",
                    "theater_name": "Bistro Screen 1",
                    "slot": "Tea Time Block (17:45)",
                    "status": "active"
                }
            ]
            for m in sample_movies:
                db.add(MovieModel(**m))
            db.commit()
    except Exception as e:
        print("Seeding error:", e)
    finally:
        db.close()

seed_database()


# ─────────────────────────────────────────────────────────────────────────────
# 🎬 MOVIES API ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/movies/available/", response_model=List[MovieResponse])
def get_available_movies(db: Session = Depends(get_db)):
    """Retrieve all available shows with status as active and seats still available."""
    return db.query(MovieModel).filter(
        MovieModel.status == "active",
        MovieModel.available_seats > 0
    ).all()


@app.get("/movies/all/", response_model=List[MovieResponse])
def get_all_movies(db: Session = Depends(get_db)):
    """Retrieve all movies, active and inactive (for Admin View)."""
    return db.query(MovieModel).all()


@app.get("/movies/search/", response_model=List[MovieResponse])
def search_movies_by_title(title: str, db: Session = Depends(get_db)):
    """Search active movies by title (substring, case-insensitive)."""
    return db.query(MovieModel).filter(
        MovieModel.status == "active",
        MovieModel.title.ilike(f"%{title}%")
    ).all()


@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/movies/", response_model=MovieResponse)
def add_new_movie(movie_in: MovieCreate, db: Session = Depends(get_db)):
    avail = movie_in.available_seats if movie_in.available_seats is not None else movie_in.total_seats
    movie_repr = MovieModel(
        title=movie_in.title,
        description=movie_in.description,
        genre=movie_in.genre,
        duration=movie_in.duration,
        rating=movie_in.rating,
        image_url=movie_in.image_url or "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&auto=format&fit=crop&q=80",
        price=movie_in.price,
        total_seats=movie_in.total_seats,
        available_seats=avail,
        show_date=movie_in.show_date,
        show_time=movie_in.show_time,
        theater_name=movie_in.theater_name or "Main Theater Lounge",
        slot=movie_in.slot or "Evening Show",
        status="active"
    )
    db.add(movie_repr)
    db.commit()
    db.refresh(movie_repr)
    return movie_repr


@app.put("/movies/{movie_id}/complete")
def complete_show(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie show not found")
    
    # Store in completed_movies archive table
    completed_movie = CompletedMovieModel(
        title=movie.title,
        description=movie.description,
        genre=movie.genre,
        duration=movie.duration,
        rating=movie.rating,
        image_url=movie.image_url,
        price=movie.price,
        total_seats=movie.total_seats,
        available_seats=movie.available_seats,
        show_date=movie.show_date,
        show_time=movie.show_time,
        theater_name=movie.theater_name,
        slot=movie.slot,
        status="completed"
    )
    db.add(completed_movie)
    
    # Remove from active MovieModel directory list
    db.delete(movie)
    db.commit()
    return {"message": "Show marked as completed and stored in database archive table successfully!"}


# ─────────────────────────────────────────────────────────────────────────────
# 👤 USERS API ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/users/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(UserModel).filter(UserModel.name.ilike(user_in.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username is already registered")
    
    new_user = UserModel(name=user_in.name, phone=user_in.phone, role=user_in.role or "user",password=pwd_context.hash(user_in.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login/", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.name.ilike(credentials.name)).first()
    if not user or not user.password:  # ← handle NULL password
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not pwd_context.verify(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return LoginResponse(id=user.id, name=user.name, role=user.role)


@app.get("/users/name/{user_name}", response_model=UserResponse)
def get_user_by_name(user_name: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.name.ilike(user_name)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()


# ─────────────────────────────────────────────────────────────────────────────
# 🎟️ BOOKINGS API ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/bookings/", response_model=BookingResponse)
def create_booking(booking_in: BookingCreate, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == booking_in.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie.status != "active":
        raise HTTPException(status_code=400, detail="This movie show is already completed")
        
    if movie.available_seats < booking_in.seats_booked:
        raise HTTPException(status_code=400, detail=f"Insufficient seats. Only {movie.available_seats} remaining.")
    
    # Generate reservation unique reference
    booking_ref = generate_booking_ref()
    while db.query(BookingModel).filter(BookingModel.booking_reference == booking_ref).first() is not None:
        booking_ref = generate_booking_ref()

    # Deduct seats from movie available inventory
    movie.available_seats -= booking_in.seats_booked
    
    new_booking = BookingModel(
        user_id=booking_in.user_id,
        movie_id=booking_in.movie_id,
        seats_booked=booking_in.seats_booked,
        booking_date=booking_in.booking_date,
        booking_time=booking_in.booking_time,
        booking_reference=booking_ref
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@app.get("/bookings/ref/{booking_reference}", response_model=BookingResponse)
def get_booking_by_ref(booking_reference: str, db: Session = Depends(get_db)):
    booking = db.query(BookingModel).filter(BookingModel.booking_reference == booking_reference).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking details not found")
    return booking


@app.get("/bookings/user/{user_id}", response_model=List[BookingResponse])
def get_bookings_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(BookingModel).filter(BookingModel.user_id == user_id).all()


@app.get("/bookings/", response_model=List[BookingResponse])
def get_all_bookings(db: Session = Depends(get_db)):
    return db.query(BookingModel).all()


@app.delete("/bookings/{booking_id}")
def cancel_booking_endpoint(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Restore available seat capacity back to the movie
    movie = db.query(MovieModel).filter(MovieModel.id == booking.movie_id).first()
    if movie:
        movie.available_seats += booking.seats_booked
    
    db.delete(booking)
    db.commit()
    return {"message": "Booking has been cancelled successfully and seats are released."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
