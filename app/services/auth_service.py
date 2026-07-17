from sqlalchemy.orm import Session
from typing import Optional

from app.models.user import User
from app.core.security import verify_password
from app.repositories.user_repository import user_repository

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        # Delegate DB lookup to repository
        user = user_repository.get_by_email(db, email=email)
        if not user:
            return None

        # Business logic: Verify password
        if not verify_password(password, user.hashed_password):
            return None

        return user
