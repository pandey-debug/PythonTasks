from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, validator
from typing import List, Optional
from sqlalchemy import Boolean, create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import random, string
from datetime import datetime

app = FastAPI()

DATABASE_URL = "mysql+pymysql://@localhost:3306/MovieTkt_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ─────────────────────────────────────────────
# 🗄️ DATABASE MODELS
# ─────────────────────────────────────────────

class User(Base):
    __tablename__ = "Users"
    id    = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name  = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20),  nullable=False, unique=True)


class Movie(Base):
    __tablename__ = "MovieTicketBookingSystem"
    id                = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title             = Column(String(255), nullable=False)
    genre             = Column(String(255), nullable=False)
    duration          = Column(Integer,     nullable=False)
    rating            = Column(Float,       nullable=False)
    ticket_price      = Column(Float,       nullable=False)
    total_tickets     = Column(Integer,     nullable=False)
    available_tickets = Column(Integer,     nullable=False)
    showtime          = Column(String(255), nullable=False)
    show_date         = Column(String(255), nullable=False)
    is_available      = Column(Boolean,     default=True)
    completed         = Column(Boolean,     default=False)


class BookingDb(Base):
    __tablename__ = "MovieBookingRecords"
    id                = Column(Integer,     primary_key=True, index=True, autoincrement=True)
    user_id           = Column(Integer,     nullable=False)
    movie_id          = Column(Integer,     nullable=False)
    seats_booked      = Column(Integer,     default=1)
    booking_reference = Column(String(20),  unique=True, nullable=False)
    booking_date      = Column(String(255), nullable=True)
    booking_time      = Column(String(255), nullable=True)
    is_active         = Column(Boolean,     default=True)


class UserBookingHistory(Base):
    __tablename__ = "UserBookingHistory"
    id                = Column(Integer,     primary_key=True, index=True, autoincrement=True)
    user_id           = Column(Integer,     nullable=False)
    movie_id          = Column(Integer,     nullable=False)
    booking_reference = Column(String(20),  nullable=False)
    seats_booked      = Column(Integer,     default=1)
    booking_date      = Column(String(255), nullable=True)
    booking_time      = Column(String(255), nullable=True)
    is_active         = Column(Boolean,     default=True)


Base.metadata.create_all(bind=engine)


# ─────────────────────────────────────────────
# 📦 PYDANTIC SCHEMAS
# ─────────────────────────────────────────────

# ── User ──
class UserSchemaCreate(BaseModel):
    name : str
    phone: str

class UserSchema(UserSchemaCreate):
    id: int
    class Config:
        orm_mode = True


# ── Movie ──
class MovieSchemaCreate(BaseModel):
    title            : str
    genre            : str
    duration         : int
    rating           : float
    ticket_price     : float
    total_tickets    : int
    available_tickets: int
    showtime         : str
    show_date        : str
    is_available     : bool = True
    completed        : bool = False

    @validator('rating')
    def rating_must_be_valid(cls, v):
        if not (0.0 <= v <= 10.0):
            raise ValueError('Rating must be between 0 and 10')
        return v

    @validator('available_tickets')
    def available_must_not_exceed_total(cls, v, values):
        if 'total_tickets' in values and v > values['total_tickets']:
            raise ValueError('available_tickets cannot exceed total_tickets')
        return v

class MovieSchema(MovieSchemaCreate):
    id: int
    class Config:
        orm_mode = True


# ── Booking ──
class BookingSchemaCreate(BaseModel):
    movie_id    : int
    user_id     : int
    seats_booked: int = 1
    booking_date: Optional[str] = None
    booking_time: Optional[str] = None

    @validator('seats_booked')
    def seats_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('seats_booked must be at least 1')
        return v

class BookingSchema(BaseModel):
    id               : int
    movie_id         : int
    user_id          : int
    seats_booked     : int
    booking_reference: str
    is_active        : bool
    booking_date     : Optional[str] = None
    booking_time     : Optional[str] = None
    class Config:
        orm_mode = True


# ── User History ──
class UserHistorySchema(BaseModel):
    id               : int
    user_id          : int
    movie_id         : int
    booking_reference: str
    seats_booked     : int
    is_active        : bool
    booking_date     : Optional[str] = None
    booking_time     : Optional[str] = None
    class Config:
        orm_mode = True


# ─────────────────────────────────────────────
# 🔧 HELPERS
# ─────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_ref_id(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# ─────────────────────────────────────────────
# 🏠 HOME
# ─────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "🎬 Movie Ticket Booking — FastAPI + MySQL"}


# ─────────────────────────────────────────────
# 👤 USER ROUTES
# ─────────────────────────────────────────────

# Register a new user
@app.post("/users/", response_model=UserSchema)
def create_user(user: UserSchemaCreate, db: Session = Depends(get_db)):
    # Check duplicate name
    if db.query(User).filter(User.name == user.name).first():
        raise HTTPException(status_code=400, detail=f"Username '{user.name}' is already taken. Please use a different name.")
    # Check duplicate phone
    if db.query(User).filter(User.phone == user.phone).first():
        raise HTTPException(status_code=400, detail="Phone number already registered.")
    db_user = User(name=user.name, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by ID
@app.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get user by name
@app.get("/users/name/{user_name}", response_model=UserSchema)
def get_user_by_name(user_name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{user_name}' not found")
    return user

# Get all users (admin)
@app.get("/users/", response_model=List[UserSchema])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# Delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": f"User '{db_user.name}' deleted successfully"}


# ─────────────────────────────────────────────
# 🎬 PHASE 1 — BROWSE
# ─────────────────────────────────────────────

# API 1 — Get all available movies
@app.get("/movies/available/", response_model=List[MovieSchema])
def get_available_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).filter(Movie.is_available == True).all()
    if not movies:
        raise HTTPException(status_code=404, detail="No available movies found")
    return movies

# API 2 — Search movie by name
@app.get("/movies/search/", response_model=List[MovieSchema])
def search_movies(title: str, db: Session = Depends(get_db)):
    movies = db.query(Movie).filter(Movie.title.ilike(f"%{title}%")).all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found with that title")
    return movies

# API 3 — Get movie details by ID (also used to check available tickets)
@app.get("/movies/{movie_id}", response_model=MovieSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


# ─────────────────────────────────────────────
# 🎟️ PHASE 2 — BOOKING
# ─────────────────────────────────────────────

# API 4 — Create a booking
@app.post("/bookings/", response_model=BookingSchema)
def create_booking(booking: BookingSchemaCreate, db: Session = Depends(get_db)):
    # Check user exists
    db_user = db.query(User).filter(User.id == booking.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with id {booking.user_id} not found. Please register first.")

    # Check movie exists
    db_movie = db.query(Movie).filter(Movie.id == booking.movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Check movie is available
    if not db_movie.is_available:
        raise HTTPException(status_code=400, detail="Movie is not available for booking")

    # Check enough tickets
    if db_movie.available_tickets < booking.seats_booked:
        raise HTTPException(
            status_code=400,
            detail=f"Only {db_movie.available_tickets} tickets available"
        )

    ref_id = generate_ref_id()

    # Save to MovieBookingRecords
    db_booking = BookingDb(
        movie_id         =booking.movie_id,
        user_id          =booking.user_id,
        booking_reference=ref_id,
        seats_booked     =booking.seats_booked,
        booking_date     =booking.booking_date,
        booking_time     =booking.booking_time,
        is_active        =True
    )
    db.add(db_booking)

    # Save to UserBookingHistory
    db_history = UserBookingHistory(
        user_id          =booking.user_id,
        movie_id         =booking.movie_id,
        booking_reference=ref_id,
        seats_booked     =booking.seats_booked,
        booking_date     =booking.booking_date,
        booking_time     =booking.booking_time,
        is_active        =True
    )
    db.add(db_history)

    # Decrement available tickets
    db_movie.available_tickets -= booking.seats_booked

    db.commit()
    db.refresh(db_booking)
    return db_booking

# API 5 — Get booking by reference ID (confirmation screen)
@app.get("/bookings/ref/{booking_reference}", response_model=BookingSchema)
def get_booking_by_reference(booking_reference: str, db: Session = Depends(get_db)):
    booking = db.query(BookingDb).filter(
        BookingDb.booking_reference == booking_reference
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

# API 6 — Get all bookings of a user by user_id
@app.get("/bookings/user/{user_id}", response_model=List[BookingSchema])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    # Check user exists
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    bookings = db.query(BookingDb).filter(BookingDb.user_id == user_id).all()
    if not bookings:
        raise HTTPException(status_code=404, detail=f"No bookings found for user '{db_user.name}'")
    return bookings

# API 6b — Get all bookings of a user by user name
@app.get("/bookings/username/{user_name}", response_model=List[BookingSchema])
def get_bookings_by_username(user_name: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user_name).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User '{user_name}' not found")
    bookings = db.query(BookingDb).filter(BookingDb.user_id == db_user.id).all()
    if not bookings:
        raise HTTPException(status_code=404, detail=f"No bookings found for '{user_name}'")
    return bookings


# ─────────────────────────────────────────────
# 🔄 PHASE 3 — CHANGES
# ─────────────────────────────────────────────

# API 7 — Get booking by booking ID
@app.get("/bookings/{booking_id}", response_model=BookingSchema)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(BookingDb).filter(BookingDb.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

# API 8 — Cancel booking by booking ID (soft delete)
@app.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(BookingDb).filter(BookingDb.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if not db_booking.is_active:
        raise HTTPException(status_code=400, detail="Booking is already cancelled")

    # Soft delete
    db_booking.is_active = False

    # Mark inactive in UserBookingHistory
    db_history = db.query(UserBookingHistory).filter(
        UserBookingHistory.booking_reference == db_booking.booking_reference
    ).first()
    if db_history:
        db_history.is_active = False

    # Restore available tickets
    db_movie = db.query(Movie).filter(Movie.id == db_booking.movie_id).first()
    if db_movie:
        db_movie.available_tickets += db_booking.seats_booked

    db.commit()
    return {
        "message"          : "Booking cancelled successfully",
        "booking_reference": db_booking.booking_reference,
        "tickets_restored" : db_booking.seats_booked
    }

# API 8b — Cancel booking by user name
@app.delete("/bookings/cancel/{user_name}")
def cancel_booking_by_username(user_name: str, db: Session = Depends(get_db)):
    # Find user by name
    db_user = db.query(User).filter(User.name == user_name).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User '{user_name}' not found")

    # Find their latest active booking
    db_booking = db.query(BookingDb).filter(
        BookingDb.user_id   == db_user.id,
        BookingDb.is_active == True
    ).order_by(BookingDb.id.desc()).first()

    if not db_booking:
        raise HTTPException(status_code=404, detail=f"No active booking found for '{user_name}'")

    # Soft delete
    db_booking.is_active = False

    # Mark inactive in UserBookingHistory
    db_history = db.query(UserBookingHistory).filter(
        UserBookingHistory.booking_reference == db_booking.booking_reference
    ).first()
    if db_history:
        db_history.is_active = False

    # Restore tickets
    db_movie = db.query(Movie).filter(Movie.id == db_booking.movie_id).first()
    if db_movie:
        db_movie.available_tickets += db_booking.seats_booked

    db.commit()
    return {
        "message"          : f"Booking cancelled for user '{user_name}'",
        "booking_reference": db_booking.booking_reference,
        "tickets_restored" : db_booking.seats_booked
    }

# API 9 — Update movie details (admin)
@app.put("/movies/{movie_id}", response_model=MovieSchema)
def update_movie(movie_id: int, movie: MovieSchemaCreate, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in movie.dict().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie


# ─────────────────────────────────────────────
# 🎬 PHASE 4 — ADMIN MANAGEMENT
# ─────────────────────────────────────────────

# API 10 — Add a new movie (admin)
@app.post("/movies/", response_model=MovieSchema)
def create_movie(movie: MovieSchemaCreate, db: Session = Depends(get_db)):
    existing = db.query(Movie).filter(
        Movie.title     == movie.title,
        Movie.show_date == movie.show_date,
        Movie.showtime  == movie.showtime
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="This show already exists")
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# API 11 — Get all movies (admin view)
@app.get("/movies/all/", response_model=List[MovieSchema])
def get_all_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found")
    return movies

# API 12 — Mark show as completed (admin)
@app.put("/movies/{movie_id}/complete")
def mark_show_completed(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    if db_movie.completed:
        raise HTTPException(status_code=400, detail="Show is already marked as completed")
    db_movie.completed    = True
    db_movie.is_available = False
    db.commit()
    return {"message": f"Show '{db_movie.title}' marked as completed"}

# API 13 — Get all bookings (admin view)
@app.get("/bookings/", response_model=List[BookingSchema])
def get_all_bookings(db: Session = Depends(get_db)):
    bookings = db.query(BookingDb).all()
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found")
    return bookings

# API 14 — Get user booking history by user_id
@app.get("/history/user/{user_id}", response_model=List[UserHistorySchema])
def get_user_history(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    history = db.query(UserBookingHistory).filter(
        UserBookingHistory.user_id == user_id
    ).all()
    if not history:
        raise HTTPException(status_code=404, detail=f"No history found for user '{db_user.name}'")
    return history

# API 14b — Get user booking history by user name
@app.get("/history/username/{user_name}", response_model=List[UserHistorySchema])
def get_user_history_by_name(user_name: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user_name).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User '{user_name}' not found")
    history = db.query(UserBookingHistory).filter(
        UserBookingHistory.user_id == db_user.id
    ).all()
    if not history:
        raise HTTPException(status_code=404, detail=f"No history found for '{user_name}'")
    return history

# API 15 — Delete a movie (admin)
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(db_movie)
    db.commit()
    return {"message": f"Movie '{db_movie.title}' deleted successfully"}