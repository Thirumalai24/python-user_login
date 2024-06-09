import os
from dotenv import load_dotenv
from fastapi import HTTPException
from typing import Optional
from pydantic import BaseModel 
from bson.objectid import ObjectId
from app.db.model_options import ModelOptions
from pydantic import BaseModel

import bcrypt

# Define the structure of user data for registration
class UsersData(BaseModel):
    first_name: str 
    last_name: str  
    email: str 
    password: str   
           

class Users:
    def __init__(self, options: ModelOptions):
        self.options = options
        self.collection = options.db["users"]
        print("\nCollection:", self.collection)

    # Convert ObjectId to string for JSON serialization
    def get_plain(self, user_data):
        user_data['_id'] = str(user_data['_id'])
        return user_data
    
    #create user
    async def create_user(self, user_data: UsersData):
        # Hash password before storing
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
        user_data.password = hashed_password.decode('utf-8')

        # Insert user data into the database
        result = await self.collection.insert_one(user_data.dict())
        return str(result.inserted_id)
    
     # check user already exists by email
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        user = await self.collection.find_one({'email': email})
        return user
    
    #Hash password 
    async def hash_password(self, password: str) -> str:
        secret_key = os.getenv('secret_key')
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(secret_key))
    
    #verify hash password
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    

    # User login
    async def login(self, login_data: dict):
        # Extract email and password from login_data
        email = login_data.get("email")
        password = login_data.get("password")
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password are required")
        
        # Find user in the database by email 
        user = await self.collection.find_one({'email': email})
        if user:
            stored_password = user.get('password')
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                # If passwords match, remove password from user data and convert ObjectId to string
                user.pop('password')  
                user['_id'] = str(user['_id'])
                return user
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
