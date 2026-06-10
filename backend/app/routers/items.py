from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ..models.user import User
from ..database import get_db
from ..repositories.permission_repository import PermissionRepository
from .dependencies import get_current_user, check_permission

router = APIRouter(prefix="/items", tags=["items"])

MOCK_ITEMS = [
    {"id": 1, "title": "Проект Alpha", "status": "active", "owner": "admin"},
    {"id": 2, "title": "Проект Beta", "status": "active", "owner": "admin"},
    {"id": 3, "title": "Задача 1", "status": "in_progress", "owner": "user"},
    {"id": 4, "title": "Задача 2", "status": "done", "owner": "user"},
    {"id": 5, "title": "Отчёт Q1", "status": "review", "owner": "admin"},
]


@router.get("/")
def get_items(
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    # Проверяем право read на ресурс items через таблицу permissions
    perm_repo = PermissionRepository(db)
    has_access = perm_repo.check_permission(
        current_user.role_id, "items", "read"
    )
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )

    if current_user.role.name == "admin":
        return MOCK_ITEMS
    else:
        return [item for item in MOCK_ITEMS if item["owner"] == "user"]


@router.get("/{item_id}")
def get_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    perm_repo = PermissionRepository(db)
    has_access = perm_repo.check_permission(
        current_user.role_id, "items", "read"
    )
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )

    item = next((i for i in MOCK_ITEMS if i["id"] == item_id), None)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект не найден",
        )

    if current_user.role.name != "admin" and item["owner"] == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )
    return item
