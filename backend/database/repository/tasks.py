from database.models.tasks import TasksORM
from database.repository.repository import SQLAlchemyRepository


class TasksRepository(SQLAlchemyRepository):
    model = TasksORM
