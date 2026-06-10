from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    resource = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    role = relationship("Role", back_populates="permissions")

    def __repr__(self):
        return f"<Permission(id={self.id}, resource='{self.resource}', action='{self.action}', role_id={self.role_id})>"
