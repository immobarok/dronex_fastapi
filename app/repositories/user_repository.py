from typing import Optional
from sqlalchemy.orm import Session

from app.repositories.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate

class CRUDUser(CRUDBase[User, UserCreate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create_user_with_hashed_password(self, db: Session, *, obj_in: UserCreate, hashed_password: str) -> User:
        db_obj = User(
            name=obj_in.name,
            email=obj_in.email,
            hashed_password=hashed_password
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user_repository = CRUDUser(User)
