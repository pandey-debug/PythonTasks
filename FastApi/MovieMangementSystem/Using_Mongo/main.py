from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mongoengine import connect, Document, IntField, StringField, BooleanField,FloatField
from urllib.parse import quote_plus


app=FastAPI()
# ------------------------------------------------------------
# 🗄️ Database Configuration# ------------------------------------------------------------
MONGO_URL = "mongodb+srv://Pandey_debug:qu7h7YRHY1bHApkF@mongodb.bpnhjid.mongodb.net/?appName=MongoDB"

connect(db="MSB_db", host=MONGO_URL)

class Movies_DB(Document):
    
    id= IntField(primary_key=True)
    name= StringField(required=True)
    genre= StringField(required=True)
    rating= FloatField(required=True)
    duration = IntField(nullable=False)
    rating=FloatField(nullable=False)
    ticket_price=FloatField(nullable=False)
    total_tickets=IntField(nullable=False)
    available_tickets=IntField(nullable=False)
    showtime=StringField(nullable=False)
    show_date=StringField(nullable=False)
    is_available=BooleanField(default=True)
    completed = BooleanField(default=False)
    
    meta={"collection":"Movies"}
# ------------------------------------------------------------
# 🧾 Pydantic Schema    
class Movie(BaseModel):
    id: int
    name: str
    genre: str
    rating: float
    duration: int
    ticket_price: float
    total_tickets: int
    available_tickets: int
    showtime: str
    show_date: str
    is_available: bool = True
    completed: bool = False 
@app.get("/")
def home():
    return {"message":"FastAPI + MongoDB Atlas 🚀"}
@app.post("/AddMovies") 
def add_movie(m_info :Movie):
    
    existing=Movies_DB.objects(id=m_info.id).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Movie with this ID already exists.")
    
    new_movie = Movies_DB(
        id=m_info.id,
        name=m_info.name,
        genre=m_info.genre,
        rating=m_info.rating,
        duration=m_info.duration,
        ticket_price=m_info.ticket_price,
        total_tickets=m_info.total_tickets,
        available_tickets=m_info.available_tickets,
        showtime=m_info.showtime,
        show_date=m_info.show_date,
        is_available=m_info.is_available,
        completed=m_info.completed
    )
    new_movie.save()
    return {"message": "Movie added successfully!"}       
#Getting all movies
@app.get("/Movies") 
def display_all_movies():
    movies = Movies_DB.objects()
    return {"movies": movies}   
# ------------------------------------------------------------
#get movie by id
@app.get("/Movies/{movie_id}")  
def get_movie_by_id(movie_id: int):
    movie = Movies_DB.objects(id=movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")
    return {"movie": movie}
# ------------------------------------------------------------
#update movie by id 
@app.put("/Movies/{movie_id}")
def update_movie(movie_id: int, m_info: Movie):
    movie = Movies_DB.objects(id=movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")
    
    movie.update(
        name=m_info.name,
        genre=m_info.genre,
        rating=m_info.rating,
        duration=m_info.duration,
        ticket_price=m_info.ticket_price,
        total_tickets=m_info.total_tickets,
        available_tickets=m_info.available_tickets,
        showtime=m_info.showtime,
        show_date=m_info.show_date,
        is_available=m_info.is_available,
        completed=m_info.completed
    )
    return {"message": "Movie updated successfully!"}       
# ------------------------------------------------------------
#delete movie by id 
@app.delete("/Movies/{movie_id}")
def delete_movie(movie_id: int):    
    movie = Movies_DB.objects(id=movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")
    
    movie.delete()
    return {"message": "Movie deleted successfully!"}

#Booking a ticket for a movie
@app.post("/Movies/{movie_id}/book")    
def book_ticket(movie_id: int):
    movie = Movies_DB.objects(id=movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")
    
    if movie.available_tickets <= 0:
        raise HTTPException(status_code=400, detail="No tickets available.")
    
    movie.update(dec__available_tickets=1)
    return {"message": "Ticket booked successfully!"}   
#
#Cancel a ticket for a movie
@app.post("/Movies/{movie_id}/cancel")  
def cancel_ticket(movie_id: int):
    movie = Movies_DB.objects(id=movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")
    
    if movie.available_tickets >= movie.total_tickets:
        raise HTTPException(status_code=400, detail="All tickets are already available.")
    
    movie.update(inc__available_tickets=1)
    return {"message": "Ticket cancellation successful!"}
# ------------------------------------------------------------
#Search movies by name  
@app.get("/Movies/search")
def search_movies(name: str):
    movies = Movies_DB.objects(name__icontains=name)
    return {"movies": movies}   
# ------------------------------------------------------------
# Get available movies
@app.get("/Movies/available")   
def get_available_movies():
    movies = Movies_DB.objects(is_available=True)
    return {"movies": movies}
# ------------------------------------------------------------
#get all shows
@app.get("/Movies/shows")
def get_all_shows():
    movies = Movies_DB.objects()
    data = []
    for st in movies:
        data.append({
            "id": st.id,
            "name": st.name,
            "genre": st.genre,
            "rating": st.rating,
            "duration": st.duration,
            "ticket_price": st.ticket_price,
            "total_tickets": st.total_tickets,
            "available_tickets": st.available_tickets,
            "showtime": st.showtime,
            "show_date": st.show_date,
            "is_available": st.is_available,
            "completed": st.completed
        })
    return {"shows": data}
