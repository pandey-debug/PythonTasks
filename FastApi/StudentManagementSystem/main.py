from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
app=FastAPI()
class std(BaseModel):
    id: int
    name: str
    age: int
    Course: str
    marks:float
std_infos=[]
@app.get("/std_infos")
def display_all():
    return std_infos


@app.get("/std_info/{id}")
def std_By_id(id:int):
    for info in std_infos:
        if info.id == id:
            return info
    return "ID Not Found"


@app.post("/std_info")
def add_std(std_info :std):
    for info in std_infos:
        if info.id == std_info.id:
            return "Id Arleady Exist"
    std_infos.append(std_info)
    return {"data":std_info,"message":"STUDENT ADDED SUCCESSFULLY"}


@app.put("/std_info/{id}")
def update_By_id(id:int,std_info :std):
    for i in range(len(std_infos)):
        if std_infos[i].id == id:
            std_infos[i]= std_info
            return std_infos 
        
         
    return "STUDENT ID NOT FOUND"


@app.delete("/std_info/{id}")
def del_by_id(id:int):
    for i in range(len(std_infos)):
        if std_infos[i].id == id:
            del std_infos[i]
            return "Student Deleted Successfully"
    return "Id Not found "
    