from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models.user import User
from ..repositories.user_repository import UserRepository
from ..repositories.permission_repository import PermissionRepository
from ..repositories.role_repository import RoleRepository
from ..services.login_service import get_current_user_id


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Необходима аутентификация",
        )

    token = authorization.split(" ")[1]
    user_id = get_current_user_id(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или просроченный токен",
        )

    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден или деактивирован",
        )
    return user


async def check_permission(
    resource: str,
    action: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    permission_repo = PermissionRepository(db)
    has_access = permission_repo.check_permission(
        user.role_id, resource, action)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Доступ запрещён: требуется право '{action}' на ресурс '{resource}'",
        )


async def require_admin(user: User = Depends(get_current_user)) -> None:
    if user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Требуется роль администратора",
        )
