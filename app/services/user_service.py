from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.repositories.user_repository import user_repository

class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        # Business logic: Check if user exists
        db_user = user_repository.get_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Business logic: Hash password
        hashed_password = get_password_hash(user.password)
        
        # Delegate DB creation to repository
        new_user = user_repository.create_user_with_hashed_password(
            db, obj_in=user, hashed_password=hashed_password
        )
        
        return new_user

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 10):
        # Delegate DB read to repository
        return user_repository.get_multi(db, skip=skip, limit=limit)
