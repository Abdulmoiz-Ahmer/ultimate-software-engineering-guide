from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


# Input payload for create command
class CreateTodoCommand(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


# Input payload for update command
class UpdateTodoCommand(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


# Immutable output DTO for queries and command results
class TodoDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    completed: bool
