from pydantic import BaseModel

class Userschema(BaseModel):
    name:str
    username:str
    password:str
    email:str


class UserResponseSchema(BaseModel):
    name:str
    username:str
    email:str
    id:int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    username:str
    password:str