from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.permission import Permission
from ..schemas.permission import PermissionCreate, PermissionUpdate


class PermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Permission]:
        return self.db.query(Permission).all()

    def get_by_id(self, permission_id: int) -> Optional[Permission]:
        return self.db.query(Permission).filter(Permission.id == permission_id).first()

    def get_by_role(self, role_id: int) -> List[Permission]:
        return self.db.query(Permission).filter(Permission.role_id == role_id).all()

    def create(self, permission_data: PermissionCreate) -> Permission:
        db_permission = Permission(**permission_data.model_dump())
        self.db.add(db_permission)
        self.db.commit()
        self.db.refresh(db_permission)
        return db_permission

    def update(self, permission_id: int, permission_data: PermissionUpdate) -> Optional[Permission]:
        db_permission = self.get_by_id(permission_id)
        if not db_permission:
            return None
        update_dict = permission_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_permission, key, value)
        self.db.commit()
        self.db.refresh(db_permission)
        return db_permission

    def delete(self, permission_id: int) -> bool:
        db_permission = self.get_by_id(permission_id)
        if not db_permission:
            return False
        self.db.delete(db_permission)
        self.db.commit()
        return True

    def check_permission(self, role_id: int, resource: str, action: str) -> bool:
        return (
            self.db.query(Permission)
            .filter(
                Permission.role_id == role_id,
                Permission.resource == resource,
                Permission.action == action,
            )
            .first()
        ) is not None
