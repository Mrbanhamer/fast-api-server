from pydantic import BaseModel
from typing import Optional

class TaskSchema(BaseModel):
    id: Optional[int] = None # Added for when you fetch tasks
    title: str
    description: Optional[str] = None
    completed: bool = False