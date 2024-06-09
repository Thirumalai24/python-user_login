
from typing import List
from fastapi import APIRouter, Request, HTTPException

from app.db.models.base import ABC
from app.db.models.users import UsersData
from app.api.schemas.responses.users import UsersResponse, CreateUserResponse
from app.api.schemas.requests.users import RegisterUsersRequest,LoginUserRequest
from app.common.errors import InternalError, NotFound

user_router = APIRouter()
login_router = APIRouter()

class BaseUser(ABC):
    pass

class Users(BaseUser):
    def __init__(self, data: UsersData):
        self.data = data

    
    # create users
    @user_router.post('/users')
    async def create_user(
        request: Request,
        data: RegisterUsersRequest
    ) -> CreateUserResponse:
        try:
            # Check if the email already exists
            user_exists = await request.app.state.models.get('users').get_user_by_email(data.email)
            if user_exists:
                return CreateUserResponse(message="User with this email already exists")
            else:
                user_data = UsersData(
                    first_name=data.first_name,
                    last_name=data.last_name,
                    email=data.email,
                    password=data.password,
                   
                )

                user_id = await request.app.state.models.get('users').create_user(user_data)
                return CreateUserResponse(id=user_id, message="User created successfully")
        except Exception as e:
            raise InternalError(["An error occurred while creating the user"])
        
# Login endpoint
@login_router.post("/login")
async def login(
    request: Request,
    login_data: LoginUserRequest
):
    try:
        user = await request.app.state.models.get('users').login(login_data.dict())
        if user:
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except Exception as e:
        raise InternalError(["An error occurred while logging in"])


       

