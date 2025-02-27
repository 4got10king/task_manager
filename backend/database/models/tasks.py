from backend.app.schemas.tasks import TasksSchema
from database.db_metadata import Base
from database.models.mixin import IsActiveMixin, TimestampMixin
from pydantic import BaseModel
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TasksORM(Base, IsActiveMixin, TimestampMixin):
    """ORM модель для таблицы tasks"""
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    def get_schema(self) -> TasksSchema:
        return TasksSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at
        )