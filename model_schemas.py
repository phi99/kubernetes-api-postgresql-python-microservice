from pydantic import BaseModel
from datetime import datetime
from typing import Optional

#Pydantic model for Request to API Server
class PostBase(BaseModel):
        title: str
        content: str
        comment: bool=False

class PostCreate(PostBase):
    pass

#Pydantic model for Response from API Server
#class Post(BaseModel):
class Post(PostBase):
        id: str
        #title: str
        #content: str
        #published: bool
        created_at: datetime
        owner_id: int
        #to use pydantic model check we need to convert from sqlalchemy model to pydantic model (dict) by using the below config
        class Config:
            orm_mode=True

class UserCreate(BaseModel):
    username: str
    #email: EmailStr
    passw: str

#API server response back to the client
class UserOut(BaseModel):
    id:int
    username:str
    created_at: datetime

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    username:str
    passw:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str]=None
