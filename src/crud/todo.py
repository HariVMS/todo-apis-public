from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.todo import TaskDB, Status
from datetime import datetime, date
from src.schemas.todo import Task
from fastapi import HTTPException

# CRUD: Create Task
def create_task(db: Session, task: Task):
    try:
        # Input Validation
        if not task.task_name:
            raise ValueError("Task name is required")
        if task.due_date and task.due_date < date.today():  # Compare with date.today()
            raise ValueError("Due date cannot be in the past")

        db_task = TaskDB(
            task_name=task.task_name,
            email=task.email,
            description=task.description,
            status=task.status,
            due_date=task.due_date,
            created_at=datetime.now(),
            priority=task.priority,
            work=task.work,
            participants=task.participants,
            is_urgent=task.is_urgent,
            price=task.price
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred while creating the task.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# CRUD: Get Task by ID
def get_task(db: Session, task_id: int):
    try:
        db_task = db.query(TaskDB).filter(TaskDB.task_id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred while fetching the task.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# CRUD: Get all Tasks
def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    try:
        tasks = db.query(TaskDB).offset(skip).limit(limit).all()
        if not tasks:
            raise HTTPException(status_code=404, detail="No tasks found")
        return tasks
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred while fetching tasks.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# CRUD: Update Task
def update_task(db: Session, task_id: int, task: Task):
    try:
        db_task = db.query(TaskDB).filter(TaskDB.task_id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        # Input Validation
        if task.due_date and task.due_date < date.today():  # Compare with date.today()
            raise ValueError("Due date cannot be in the past")

        # Update fields
        db_task.task_name = task.task_name
        db_task.email = task.email
        db_task.description = task.description
        db_task.status = task.status
        db_task.due_date = task.due_date
        db_task.priority = task.priority
        db_task.work = task.work
        db_task.participants = task.participants
        db_task.is_urgent = task.is_urgent
        db_task.price = task.price
        
        db.commit()
        db.refresh(db_task)
        return db_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred while updating the task.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# CRUD: Delete Task
def delete_task(db: Session, task_id: int):
    try:
        db_task = db.query(TaskDB).filter(TaskDB.task_id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        db.delete(db_task)
        db.commit()
        return db_task
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred while deleting the task.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
