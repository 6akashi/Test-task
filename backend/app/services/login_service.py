from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..config import settings
from ..repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(
            minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def authenticate_user(db: Session, email: str, password: str) -> Optional[dict]:
    repo = UserRepository(db)
    user = repo.get_by_email(email)

    if not user or not pwd_context.verify(password, user.password):
        return None

    if not user.is_active:
        return None

    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


def get_current_user_id(token: str) -> Optional[int]:
    """Декодирует JWT и возвращает user_id (sub)."""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None
