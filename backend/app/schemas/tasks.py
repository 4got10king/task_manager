from datetime import datetime
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """Базовая схема для задачи"""
    title: str = Field(..., max_length=255)
    description: str | None = Field(None, max_length=1024)


class TaskCreate(TaskBase):
    """Схема для создания задачи"""
    pass


class TaskUpdate(TaskBase):
    """Схема для обновления задачи"""
    title: str | None = Field(None, max_length=255)


class TaskResponse(TaskBase):
    """Схема для ответа с задачей"""
    id: int
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    """Схема для списка задач"""
    items: list[TaskResponse]
    total: int