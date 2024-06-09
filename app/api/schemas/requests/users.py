import re
from pydantic import BaseModel, Field, field_validator

#create user request
class RegisterUsersRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(...)
    password: str = Field(..., min_length=8, max_length=64)
    
    #first_name, last_name validation
    @field_validator('first_name', 'last_name')
    def validate_name(cls, v):
        if not re.match("^[a-zA-Z]+$", v):
            raise ValueError("Name must contain only alphabetic characters.")
        return v
    
    # Email validation
    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format.')
        if not v.endswith('.com'):
            raise ValueError('Email must be from .com domain.')
        return v
    
    
    # Password vaidation
    @field_validator("password")
    def password_must_contain_special_characters(cls, v):
        if not re.search(r"[^a-zA-Z0-9]", v):
            raise ValueError("Password must contain special characters")
        return v

    @field_validator("password")
    def password_must_contain_numbers(cls, v):
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain numbers")
        return v

    @field_validator("password")
    def password_must_contain_uppercase(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase characters")
        return v

    @field_validator("password")
    def password_must_contain_lowercase(cls, v):
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase characters")
        return v

# user login request
class LoginUserRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=64)
    
    # Email validation
    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format.')
        if not v.endswith('.com'):
            raise ValueError('Email must be from .com domain.')
        return v



    
   
    
    


  