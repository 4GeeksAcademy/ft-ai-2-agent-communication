from fastapi import APIRouter, Depends

from area_todo_api.dependencies import get_todo_service
from area_todo_api.schemas.todo import TodoCreate, TodoRead
from area_todo_api.services.todo_service import TodoService

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])


@router.get("", response_model=list[TodoRead])
def list_todos(
    service: TodoService = Depends(get_todo_service),
) -> list[TodoRead]:
    return service.list_todos()


@router.post("", response_model=TodoRead, status_code=201)
def create_todo(
    payload: TodoCreate,
    service: TodoService = Depends(get_todo_service),
) -> TodoRead:
    return service.create_todo(payload)
