from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100,
                      description="Role Name")


class RoleCreate(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: int = Field(..., description="Unique Role ID")

    class Config:
        form_attributes = True
