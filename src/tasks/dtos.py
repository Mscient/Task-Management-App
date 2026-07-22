from fastapi import FastAPI 
from pydantic import BaseModel

class TaskSchema(BaseModel):
    title:str
    description:str
    is_Completed:bool=False


class TaskOutSchema(BaseModel):
    id:int
    title:str
    description:str
    is_Completed:bool
    user_id:int | None=0
    
    

