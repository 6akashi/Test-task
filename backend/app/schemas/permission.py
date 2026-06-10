from typing import Optional

from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    resource: str = Field(..., min_length=1, max_length=100,
                          description="Resource name (e.g. 'items')")
    action: str = Field(..., min_length=1, max_length=50,
                        description="Action (e.g. 'read', 'write', 'delete')")
    role_id: int = Field(..., description="Role ID")


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    resource: Optional[str] = Field(None, min_length=1, max_length=100)
    action: Optional[str] = Field(None, min_length=1, max_length=50)
    role_id: Optional[int] = Field(None)


class PermissionResponse(PermissionBase):
    id: int = Field(..., description="Unique Permission ID")

    class Config:
        from_attributes = True
