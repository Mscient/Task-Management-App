from fastapi import APIRouter,Depends,status
from src.tasks import controller
from src.tasks.dtos import TaskSchema,TaskOutSchema
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session
from src.utils.helper import is_authentication
from src.user.models import UserModel

task_routes=APIRouter(prefix="/tasks")



@task_routes.post("/create",response_model=TaskOutSchema,status_code=status.HTTP_201_CREATED)
def create_task(body:TaskSchema,db:Session=Depends(get_db),user:UserModel=Depends(is_authentication)):
    return controller.create_task(body,db,user)

@task_routes.get("/all_tasks",response_model=List[TaskOutSchema],status_code=status.HTTP_200_OK)
def get_all_tasks(db:Session=Depends(get_db),user:UserModel=Depends(is_authentication)):
    return controller.get_tasks(db,user)

@task_routes.get("/get_one_tasks/{task_id}",response_model=TaskOutSchema,status_code=status.HTTP_200_OK)
def get_one_tasks(task_id:int,db:Session=Depends(get_db),user:UserModel=Depends(is_authentication)):
    return controller.get_task(task_id,db)

@task_routes.put("/update/{task_id}", response_model=TaskOutSchema, status_code=status.HTTP_201_CREATED)
def update_task(task_id:int,body:TaskSchema,db:Session=Depends(get_db),user:UserModel=Depends(is_authentication)):
    return controller.update_Task(task_id,db,body,user)
    

@task_routes.delete("/delete/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int,db:Session=Depends(get_db),user:UserModel=Depends(is_authentication)):
    return controller.delete(task_id,db,user)




