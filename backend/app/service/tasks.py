from app.schemas.tasks import TasksCreate, TasksUpdate, TasksResponse, TasksList
from database.unitofwork import IUnitOfWork, UnitOfWork
from fastapi import HTTPException


class TasksService:
    @classmethod
    async def get_all_tasks(cls, uow: IUnitOfWork = UnitOfWork()) -> TasksList:
        async with uow:
            tasks = await uow.tasks.get_all()
            tasks_list = [TasksResponse.model_validate(task) for task in tasks]
            return TasksList(items=tasks_list, total=len(tasks_list))

    @classmethod
    async def get_task_by_id(cls, task_id: int, uow: IUnitOfWork = UnitOfWork()) -> TasksResponse:
        async with uow:
            task = await uow.tasks.get_by_id(task_id)
            if not task:
                raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
            return TasksResponse.model_validate(task)

    @classmethod
    async def create_task(cls, task_data: TasksCreate, uow: IUnitOfWork = UnitOfWork()) -> TasksResponse:
        async with uow:
            task = await uow.tasks.add_one(task_data.model_dump())
            await uow.commit()
            return TasksResponse.model_validate(task)

    @classmethod
    async def update_task(cls, task_id: int, task_data: TasksUpdate, uow: IUnitOfWork = UnitOfWork()) -> TasksResponse:
        async with uow:
            task = await uow.tasks.get_by_id(task_id)
            if not task:
                raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

            updated_task = await uow.tasks.edit_one(task_id, task_data.model_dump())
            await uow.commit()
            return TasksResponse.model_validate(updated_task)

    @classmethod
    async def delete_task(cls, task_id: int, uow: IUnitOfWork = UnitOfWork()) -> bool:
        async with uow:
            task = await uow.tasks.get_by_id(task_id)
            if not task:
                raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

            await uow.tasks.delete(id=task_id)
            await uow.commit()
            return True
