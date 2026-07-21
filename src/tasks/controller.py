from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException



def create_task(body:TaskSchema,db:Session):
    data=body.model_dump()
    new_task=TaskModel(title=data["title"],
                        description=data["description"],
                        is_Completed=data["is_Completed"]
                        )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task



def get_tasks(db:Session):
    tasks=db.query(TaskModel).all()
    return tasks

    
def get_task(task_id:int,db:Session):
    one_tasks=db.query(TaskModel).get(task_id)
    if not one_tasks:
        raise HTTPException(status_code=404,detail="Task Id incorrect")
    return one_tasks


def update_Task(task_id:int,db:Session,body:TaskSchema):
    one_Task=db.query(TaskModel).get(task_id)
    if not one_Task:
        raise HTTPException(status_code=404,detail="Task not found")
    body_data=body.model_dump()
    for field,value in body_data.items():
        setattr(one_Task,field,value)
    db.add(one_Task)
    db.commit()
    db.refresh(one_Task)

    return one_Task


def delete(task_id:int,db:Session):
    one_task=db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(status_code=404,detail="Task not found")
    db.delete(one_task)
    db.commit()
    return {"status": "Task deleted successfully"}
