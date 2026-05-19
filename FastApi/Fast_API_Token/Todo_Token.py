# ============================================================
# 🔐 FastAPI TODO App + JWT Authentication (Array Version)
# ============================================================

# ============================================================
# 🚀 WHAT WE ARE BUILDING
# ============================================================

'''
This project includes:

✅ FastAPI
✅ JWT Authentication
✅ CRUD Operations
✅ Temporary Storage using Python List
✅ Protected APIs using Token

No Database used here.
Data will be stored temporarily in array/list.
'''

# ============================================================
# 🚀 INSTALL REQUIRED PACKAGES
# ============================================================

'''
pip install fastapi uvicorn python-jose'''

# ============================================================
# 🧾 IMPORTING REQUIRED MODULES 
# ============================================================
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
app = FastAPI()
# ============================================================
# 🔐 JWT CONFIGURATION  
# ============================================================
SECRET_KEY="TeRrIiV14"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=10
# 
# 
# 


# ------------------------------------------------------------
# 🗄️ Database Configuration
# ------------------------------------------------------------
# Replace with your actual connection details if needed.
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/Jwt_Tododb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# ------------------------------------------------------------
# 🧱 Database Model (Table)
# ------------------------------------------------------------
class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True,autoincrement=False)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False)

# Create table
Base.metadata.create_all(bind=engine)
# ------------------------------------------------------------
# 🧾 Pydantic Schema
# ------------------------------------------------------------
class Todo(BaseModel):
    id: Optional[int]
    title: str
    completed: bool = False

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str
# ------------------------------------------------------------
# 🔌 Dependency (DB Session)
# ------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Create JWT Token 
def create_access_token(data: dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})   

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)        
    return encoded_jwt
# ============================================================
# 🔐 TOKEN VALIDATION
# ============================================================
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/login")
def verify_token(token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
# ------------------------------------------------------------
# 🏠 Home Route
# ------------------------------------------------------------
@app.get("/")
def home():
    return {"Message":"FASTAPI To DataBase"}

# login users
users = {
    "admin": "admin123",
    "tarun": "tarun123",
    "user1": "pass123"
}

@app.post("/login")
def login(user: Login):

    if user.username not in users or users[user.username] != user.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": "10 MINUTES"
    }

# ------------------------------------------------------------
# ✅ 1. CREATETODO
# ------------------------------------------------------------
#Now Lets Apply the CRUD Operatioins
@app.post("/todos")
def create_todo(todo: Todo, db: Session = Depends(get_db), user: str = Depends(verify_token)):
    existing = db.query(TodoDB).filter(TodoDB.id == todo.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="ID already exists")
    

    new_todo = TodoDB(
        #id=todo.id,
        title=todo.title,
        completed=todo.completed
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return {
        "message": "Todo created",
        "data": new_todo
    }

# ------------------------------------------------------------
# ✅ 2. READ ALL TODOS
# ------------------------------------------------------------
@app.get("/todos")
def get_all_todos(
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)
):
    todos = db.query(TodoDB).all()
    return {"count": len(todos), "data": todos}

# ------------------------------------------------------------
# ✅ 3. READ SINGLETODO
# ------------------------------------------------------------
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db), user: str = Depends(verify_token)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo



# ------------------------------------------------------------
# ✅ 4. UPDATETODO
# ------------------------------------------------------------
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated: Todo, db: Session = Depends(get_db), user: str = Depends(verify_token)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = updated.title
    todo.completed = updated.completed

    db.commit()
    db.refresh(todo)

    return {"message": "Updated successfully", "data": todo}

# ------------------------------------------------------------
# ✅ 5. DELETETODO
# ------------------------------------------------------------
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), user: str = Depends(verify_token)):    
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()

    return {"message": "Deleted successfully"}
   