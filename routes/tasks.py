from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import sql_connector as db  # Using the connector we've been fixing

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# --- Pydantic Schema ---
class TaskSchema(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# 1. CREATE
@router.post("/")
async def create_task(request: Request, task: TaskSchema):
    ticket = request.cookies.get("session_ticket")
    user_id = db.get_user_id_from_ticket(ticket)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    success = db.create_task(user_id, task.title, task.description)
    if success:
        return {"message": "Task created successfully"}
    raise HTTPException(status_code=400, detail="Failed to create task")

# 2. READ (ALL)
@router.get("/")
async def read_all(request: Request):
    ticket = request.cookies.get("session_ticket")
    user_id = db.get_user_id_from_ticket(ticket)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return db.get_all_tasks(user_id)

# 3. READ (ONE)
@router.get("/{task_id}")
async def read_one(request: Request, task_id: int):
    ticket = request.cookies.get("session_ticket")
    user_id = db.get_user_id_from_ticket(ticket)
    
    task = db.get_one_task(task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# 4. UPDATE
@router.put("/{task_id}")
async def update(request: Request, task_id: int, task: TaskSchema):
    ticket = request.cookies.get("session_ticket")
    user_id = db.get_user_id_from_ticket(ticket)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    db.update_task(task_id, user_id, task.completed)
    return {"message": "Task updated"}

# 5. DELETE
@router.delete("/{task_id}")
async def delete(request: Request, task_id: int):
    ticket = request.cookies.get("session_ticket")
    user_id = db.get_user_id_from_ticket(ticket)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    db.delete_task(task_id, user_id)
    return {"message": "Task deleted"}