from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import List
app=FastAPI()
@app.get("/")
def home():
    return {"Message":"Hello I'M new to FASTAPI"}
#Now Lets Apply the CRUD Operatioins
class Todo(BaseModel):
    id:int
    title:str
    Completed: bool = False
#The above lines ensure the Data Validation and Documentation
todos=[] #Because we are not using any DateBase now just for storing
@app.post("/A")
def create_post(todo:Todo):
    todo_dict = todo.model_dump() 
    todos.append(todo_dict)
    return{"message":"todo created","data":todo.model_dump()}
@app.get("/todos")
def get_todos():
    return todos


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")




@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos[index] = updated_todo
        return {"message": "Updated successfully", "data": updated_todo}
    raise HTTPException(status_code=404, detail="Todo not found")




@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            deleted = todos.pop(index)
            return {"message": "Deleted successfully", "data": deleted}
    raise HTTPException(status_code=404, detail="Todo not found")

