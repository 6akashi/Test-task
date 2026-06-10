from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserResponse


def register_user(db: Session, user_data: UserCreate) -> UserResponse:
    repo = UserRepository(db)
    existing = repo.get_by_email(user_data.email)
    if existing:
        raise ValueError("Пользователь с таким email уже существует")
    user = repo.create(user_data)
    return UserResponse.model_validate(user)
