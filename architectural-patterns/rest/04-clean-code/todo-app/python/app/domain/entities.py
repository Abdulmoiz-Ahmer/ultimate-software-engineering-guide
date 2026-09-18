from dataclasses import dataclass, field
import uuid
from uuid import UUID


@dataclass
class TodoEntity:
    title: str
    description: str | None = None
    completed: bool = False
    id: UUID = field(default_factory=uuid.uuid4)

    def mark_completed(self) -> None:
        self.completed = True

    def update_title(self, new_title: str) -> None:
        if not new_title.strip():
            raise ValueError("Title cannot be empty.")
        self.title = new_title
