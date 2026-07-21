from fastapi import Depends
from sqlmodel import Session

from area_todo_api.db import get_session
from area_todo_api.repositories.todo_repository import TodoRepository
from area_todo_api.services.todo_service import TodoService


def get_todo_repository(
    session: Session = Depends(get_session),
) -> TodoRepository:
    return TodoRepository(session)


def get_todo_service(
    repository: TodoRepository = Depends(get_todo_repository),
) -> TodoService:
    return TodoService(repository)
