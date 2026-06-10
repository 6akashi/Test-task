from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.role import Role
from ..schemas.role import RoleCreate


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Role]:
        return self.db.query(Role).all()

    def get_by_id(self, role_id: int) -> Optional[Role]:
        return self.db.query(Role).filter(Role.id == role_id).first()

    def get_by_name(self, role_name) -> Optional[Role]:
        return self.db.query(Role).filter(Role.name == role_name).first()

    def create(self, role_data: RoleCreate) -> Role:
        db_role = Role(**role_data.model_dump())
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role
