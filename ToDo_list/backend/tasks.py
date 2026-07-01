from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Task
from schemas import TaskCreate, TaskUpdate, Task as TaskSchema
from auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("", response_model=List[TaskSchema])
async def get_tasks(search: Optional[str] = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    query = db.query(Task)
    if search:
        query = query.filter(
            Task.title.contains(search) |
            Task.description.contains(search)
        )
    return query.all()

@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(task_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskSchema)
async def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return None