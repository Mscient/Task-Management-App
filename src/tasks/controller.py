from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException
from src.user.models import UserModel


def create_task(body:TaskSchema,db:Session,user:UserModel):
    data=body.model_dump()
    new_task=TaskModel(title=data["title"],
                        description=data["description"],
                        is_Completed=data["is_Completed"],
                        user_id=user.id
                        )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task




def get_tasks(db:Session,user:UserModel):
    tasks=db.query(TaskModel).filter(TaskModel.user_id==user.id).all()
    return tasks

    
def get_task(task_id:int,db:Session):
    one_tasks=db.query(TaskModel).get(task_id)
    if not one_tasks:
        raise HTTPException(status_code=404,detail="Task Id incorrect")
    return one_tasks


def update_Task(task_id:int,db:Session,body:TaskSchema,user:UserModel):
    one_Task:TaskModel=db.query(TaskModel).get(task_id)
    if not one_Task:
        raise HTTPException(status_code=404,detail="Task not found")
    if one_Task.user_id!=user.id:
        raise HTTPException(status_code=403,detail="You can not update this task")

    body_data=body.model_dump()
    for field,value in body_data.items():
        setattr(one_Task,field,value)
    db.add(one_Task)
    db.commit()
    db.refresh(one_Task)

    return one_Task


def delete(task_id:int,db:Session,user:UserModel):
    one_task=db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(status_code=404,detail="Task not found")
    if one_task.user_id!=user.id:
        raise HTTPException(status_code=403,detail="You can not delete this task")
    db.delete(one_task)
    db.commit()
    return {"status": "Task deleted successfully"}
