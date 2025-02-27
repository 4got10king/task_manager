from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["CRUD to tasks"])

@router.get("")
async def get_one_task():
    """
    Возвращает список всех задач из базы данных.
    """
    pass

@router.get("/{task_id}")
async def get_tasks():
    """
    Возвращает задачу по task_id.
    Если задача не найдена, возвращает 404 Not Found.
    
    Аргументы:
        task_id (int): id задачи для получения
    """
    pass

@router.post("")
async def post_tasks():
    """
    Принимает JSON с данными о задаче.
    Возвращает id созданной задачи.
    """ 
    pass

@router.put("/{task_id}")
async def put_tasks(task_id: int):
    """
    Принимает JSON с обновленными данными задачи.
    Возвращает полностью обновленную задачу.
    Если задача не найдена, возвращает 404 Not Found.
    
    Аргументы:
        task_id (int): id задачи, которуб нужно обновить
    """
    pass

@router.delete("/{task_id}")
async def delete_task(task_id: int):
    """
    Удаляет задачу из базы данных.
    Ничего не возвращает в теле ответа.

    Аргументы:
        task_id (int): id задачи, которую нужно удалить
    """
    pass