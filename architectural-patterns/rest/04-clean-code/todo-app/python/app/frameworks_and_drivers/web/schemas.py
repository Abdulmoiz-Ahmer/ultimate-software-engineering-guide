# app/frameworks_and_drivers/web/schemas.py
from uuid import UUID
from pydantic import BaseModel, Field


class CreateTodoHTTPPayload(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class UpdateTodoHTTPPayload(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


class TodoHTTPResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    completed: bool
