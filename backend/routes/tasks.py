from fastapi import APIRouter, Request, HTTPException, status
from schemas.task_schemas import TaskSchema
from database import sql_connector as db

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# 1. CREATE
@router.post("/")
async def create_task(request: Request, task: TaskSchema):
    ticket = request.cookies.get("session_ticket")
    user_id = db.get_user_id_from_ticket(ticket)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Validation happens automatically because of 'task: TaskSchema'
    success = db.create_task(user_id, task.title, task.description)
    if success:
        return {"message": "Task created successfully"}
    raise HTTPException(status_code=400, detail="Failed to create task")

# 2. READ (ALL)
@router.get("/")
async def read_all(request: Request):
    ticket = request.cookies.get("session_ticket")
    
    # 1. Check if cookie exists
    if ticket is None:
        raise HTTPException(status_code=401, detail="No session cookie found")

    user_id = db.get_user_id_from_ticket(ticket)
    
    # 2. Check if ticket is actually valid in the DB
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    return db.get_all_tasks(user_id)

# 3. READ (ONE)
@router.get("/{task_id}")
async def read_one(request: Request, task_id: int):
    ticket = request.cookies.get("session_ticket")
    user_id = db.get_user_id_from_ticket(ticket)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not authenticated"
        )
    
    task = db.get_one_task(task_id, user_id)
    
    if not task:
        # Teacher requirement: Proper HTTP 404 handling
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with ID {task_id} not found"
        )
        
    return task

# 4. UPDATE
@router.put("/{task_id}")
async def update(request: Request, task_id: int, task: TaskSchema):
    ticket = request.cookies.get("session_ticket")
    user_id = db.get_user_id_from_ticket(ticket)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    # Send the update to your SQL connector
    success = db.update_task(task_id, user_id, task.completed)
    
    if success:
        return {"message": "Task updated"}
    raise HTTPException(status_code=400, detail="Update failed")

# 5. DELETE
@router.delete("/{task_id}")
async def delete(request: Request, task_id: int):
    ticket = request.cookies.get("session_ticket")
    user_id = db.get_user_id_from_ticket(ticket)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    db.delete_task(task_id, user_id)
    return {"message": "Task deleted"}