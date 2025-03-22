from pydantic import BaseModel, PrivateAttr
import uuid

class Users(BaseModel):
    username: str 
    password: str
    