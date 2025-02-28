from fastapi import APIRouter
from app.schemas.tasks import TasksCreate, TasksUpdate, TasksResponse, TasksList
from app.service.tasks import TasksService

router = APIRouter(prefix="/tasks", tags=["CRUD to tasks"])


@router.get("", response_model=TasksList)
async def get_tasks() -> TasksList:
    """Получение списка всех задач"""
    return await TasksService.get_all_tasks()


@router.get("/{task_id}", response_model=TasksResponse)
async def get_tasks_by_id(task_id: int) -> TasksResponse:
    """Получение задачи по id"""
    return await TasksService.get_task_by_id(task_id)


@router.post("", response_model=TasksResponse, status_code=201)
async def create_tasks(task_data: TasksCreate) -> TasksResponse:
    """Создание новой задачи"""
    return await TasksService.create_task(task_data)


@router.put("/{task_id}", response_model=TasksResponse)
async def update_tasks(task_id: int, task_data: TasksUpdate) -> TasksResponse:
    """Обновление задачи"""
    return await TasksService.update_task(task_id, task_data)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int) -> None:
    """Удаление задачи"""
    return await TasksService.delete_task(task_id)
