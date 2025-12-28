# FastAPI TODO API  
A simple and efficient **Task Management REST API** built using **FastAPI**, **SQLite**, and **SQLAlchemy**.  
This project allows users to create, read, update, and delete tasks with ease.

---

##  Overview
- **Backend:** FastAPI (Python)
- **Database:** SQLite (with SQLAlchemy ORM)
- **Purpose:** Manage tasks (todos) with CRUD operations

---

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic (inside app)
- Uvicorn (server)

### Database
- SQLite (`todos.db`)

---

##  Project Structure

```
fastapi-todo/
│
├── api/
│   ├── app.py           
│   ├── database.py      
│   └── models.py        
│
├── todos.db             
├── run.py            
└── requirements.txt     
```

Windows:
```powershell
pip install -r requirements.txt
```
Run the Application
Windows:
```powershell
python run.py
```
## Access API

Swagger Documentation:  
http://localhost:8000/docs

Base URL:  
http://localhost:8000/

---
