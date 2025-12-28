from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime
from database import init_db, get_db
from models import Todo

app = FastAPI(title="Todo API", version="1.0.0")


init_db()

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class DeleteConfirm(BaseModel):
    confirm: bool = True

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


@app.get("/")
def root():
    return {"message": "Welcome to Todo API"}

@app.get("/todos", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    """Get all todos"""
    return db.query(Todo).all()

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo by ID"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos", status_code=201)
def create_todo(todo: Union[TodoCreate, List[TodoCreate]], db: Session = Depends(get_db)):
    """Create one or multiple todos"""

    if isinstance(todo, TodoCreate):
        new_todo = Todo(title=todo.title, description=todo.description)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    

    created_todos = []
    for todo_item in todo:
        new_todo = Todo(title=todo_item.title, description=todo_item.description)
        db.add(new_todo)
        created_todos.append(new_todo)
    
    db.commit()

    for todo_item in created_todos:
        db.refresh(todo_item)
    
    return created_todos

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """Update a todo - can update just ID with completed status, or title/description as needed"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.completed is not None:
        todo.completed = todo_update.completed
    
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, confirm: DeleteConfirm, db: Session = Depends(get_db)):
    """Delete a todo - requires confirmation"""
    if not confirm.confirm:
        raise HTTPException(status_code=400, detail="Delete not confirmed")
    
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return None
