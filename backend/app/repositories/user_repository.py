from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from passlib.context import CryptContext
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[User]:
        return self.db.query(User).options(joinedload(User.role)).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return (
            self.db.query(User)
            .options(joinedload(User.role))
            .filter(User.id == user_id)
            .first()
        )

    def get_by_role(self, user_role) -> List[User]:
        return (
            self.db.query(User)
            .options(joinedload(User.role))
            .filter(User.role_id == user_role)
            .all()
        )

    def get_by_email(self, email) -> Optional[User]:
        return (
            self.db.query(User)
            .options(joinedload(User.role))
            .filter(User.email == email)
            .first()
        )

    def create(self, user_data: UserCreate) -> User:
        user_dict = user_data.model_dump()
        user_dict["password"] = pwd_context.hash(user_dict["password"])
        db_user = User(**user_dict)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        update_dict = user_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def soft_delete(self, user_id: int) -> Optional[User]:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        db_user.is_active = False
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
