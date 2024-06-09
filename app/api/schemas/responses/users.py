from typing import Optional
from pydantic import BaseModel, Field


class UsersResponse(BaseModel):
    id: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    

class CreateUserResponse(BaseModel):
    id: Optional[str] = None
    message: str
         

class LoginUserResponse(BaseModel):
     message:str
     