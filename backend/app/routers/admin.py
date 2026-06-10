from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.permission import (
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse,
)
from ..repositories.permission_repository import PermissionRepository
from ..repositories.role_repository import RoleRepository
from .dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/permissions", response_model=List[PermissionResponse])
def get_permissions(
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    repo = PermissionRepository(db)
    return repo.get_all()


@router.post("/permissions", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
def create_permission(
    permission_data: PermissionCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    repo = PermissionRepository(db)
    role_repo = RoleRepository(db)
    role = role_repo.get_by_id(permission_data.role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Роль не найдена",
        )
    return repo.create(permission_data)


@router.put("/permissions/{permission_id}", response_model=PermissionResponse)
def update_permission(
    permission_id: int,
    permission_data: PermissionUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    repo = PermissionRepository(db)
    updated = repo.update(permission_id, permission_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Право доступа не найдено",
        )
    return updated


@router.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    repo = PermissionRepository(db)
    deleted = repo.delete(permission_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Право доступа не найдено",
        )
