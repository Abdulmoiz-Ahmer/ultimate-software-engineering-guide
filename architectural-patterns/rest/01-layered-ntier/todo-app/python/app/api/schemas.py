from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class TodoUpdate(BaseModel):
    title: str = Field(None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    completed: bool
