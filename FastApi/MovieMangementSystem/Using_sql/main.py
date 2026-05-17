from fastapi import FastAPI,HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import Boolean, create_engine, Column, Integer, String,Float
from sqlalchemy.orm import declarative_base     
from sqlalchemy.orm import sessionmaker, Session
app= FastAPI()
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/MovieTkt_db"
engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base() 
class Movie(Base):
    __tablename__ = "MovieTicketBookingSystem"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    genre = Column(String(255), nullable=False)
    duration = Column(Integer, nullable=False)
    rating=Column(Float,nullable=False)
    ticket_price=Column(Float,nullable=False)
    total_tickets=Column(Integer,nullable=False)
    available_tickets=Column(Integer,nullable=False)
    showtime=Column(String(255),nullable=False)
    show_date=Column(String(255),nullable=False)
    is_available=Column(Boolean, default=True)
    completed = Column(Boolean, default=False)
class BookingDb(Base):
    __tablename__ = "MovieBookingRecords"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    movie_id = Column(Integer, nullable=False)
    seats_booked = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)  
Base.metadata.create_all(bind=engine) 
class MovieSchema(BaseModel):
    id: int 
    title: str
    genre: str
    duration: int
    rating: float
    ticket_price: float
    total_tickets: int
    available_tickets: int
    showtime: str
    show_date: str
    is_available: bool= True
    completed: bool= False
class BookingSchema(BaseModel):
    id: int
    movie_id: int
    seats_booked: int
    is_active: bool = True
    class Config:
        orm_mode = True

class BookingSchemaCreate(BaseModel):
    movie_id: int
    seats_booked: int = 1
    is_active: bool = True
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Displaying The Home Page        
@app.get("/")
def home():
    return {"message": "Movie Ticket Booking FastAPI DB"}                           


#Creating A Movie
@app.post("/movies/", response_model=MovieSchema)
def create_movie(movie: MovieSchema, db: Session = Depends(get_db)):
    db_movie = Movie(
        title=movie.title,
        genre=movie.genre,
        duration=movie.duration,
        rating=movie.rating,
        ticket_price=movie.ticket_price,
        total_tickets=movie.total_tickets,
        available_tickets=movie.available_tickets,
        showtime=movie.showtime,
        show_date=movie.show_date,
        is_available=movie.is_available,
        completed=movie.completed
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie
#Getting All Movies
@app.get("/movies/",response_model=List[MovieSchema])
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()
#Getting a Movie By ID
@app.get("/movies/{movie_id}",response_model=MovieSchema )
def get_movie(movie_id:int,db: Session=Depends(get_db)):
    movie=db.query(Movie).filter(Movie.id==movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
#Update Movie DetailS
@app.put("/movies/{movie_id}",response_model=MovieSchema)
def update_movie(movie_id:int, movie: MovieSchema,  db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in movie.dict().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie
#Delete A Movie
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(db_movie)
    db.commit()
    return {"message": "Movie deleted successfully"}
#Booking A Movie Ticket
@app.post("/bookings/", response_model=BookingSchema)
def create_booking(booking: BookingSchemaCreate, db: Session = Depends(get_db)):
    db_booking = BookingDb(
        movie_id=booking.movie_id,
        seats_booked=booking.seats_booked,
        is_active=booking.is_active
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
#Cancel A Booking
@app.delete("/bookings/{booking_id}")   
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(BookingDb).filter(BookingDb.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(db_booking)
    db.commit()
    return {"message": "Booking cancelled successfully"}
#get available Shows
@app.get("/movies/available/", response_model=List[MovieSchema])    
def get_available_movies(db: Session = Depends(get_db)):
    return db.query(Movie).filter(Movie.is_available == True).all()
#Get all Shows
@app.get("/movies/all/", response_model=List[MovieSchema])
def get_all_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()    
#search movie by name
@app.get("/movies/search/", response_model=List[MovieSchema])
def search_movies(title: str, db: Session = Depends(get_db)):
    return db.query(Movie).filter(Movie.title.ilike(f"%{title}%")).all()    
