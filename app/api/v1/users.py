from app.api.deps import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, UserResponse
from app.api.deps import get_db
from app.services.user_service import UserService

from app.schemas.response import StandardResponse

router = APIRouter()

@router.post("", response_model=StandardResponse[UserResponse])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user securely. All business logic is delegated to the Service Layer.
    """
    new_user = UserService.create_user(db, user)
    return StandardResponse(
        success=True,
        message="User registered successfully",
        data=new_user
    )

@router.get("", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve users. Logic is delegated to the Service Layer.
    """
    return UserService.get_users(db, skip=skip, limit=limit)

@router.get("/me",response_model=StandardResponse[UserResponse])
def get_user_me(current_user = Depends(get_current_user)):
    return StandardResponse(
        success=True,
        message="Profile fetched successfully",
        data=current_user
    )
