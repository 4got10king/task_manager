from datetime import datetime
from pydantic import BaseModel, Field


class TasksBase(BaseModel):
    """Базовая схема для задачи"""

    title: str = Field(..., max_length=255)
    description: str | None = Field(None, max_length=1024)


class TasksCreate(TasksBase):
    """Схема для создания задачи"""

    pass


class TasksUpdate(TasksBase):
    """Схема для обновления задачи"""

    title: str | None = Field(None, max_length=255)


class TasksResponse(TasksBase):
    """Схема для ответа с задачей"""

    id: int
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TasksList(BaseModel):
    """Схема для списка задач"""

    items: list[TasksResponse]
    total: int
