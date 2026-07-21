from area_todo_api.models.todo import Todo
from area_todo_api.repositories.todo_repository import TodoRepository
from area_todo_api.schemas.todo import TodoCreate, TodoRead


class TodoService:
    def __init__(self, repository: TodoRepository) -> None:
        self.repository = repository

    def list_todos(self) -> list[TodoRead]:
        todos = self.repository.list_all()
        return [TodoRead.model_validate(todo) for todo in todos]

    def create_todo(self, payload: TodoCreate) -> TodoRead:
        todo = Todo.model_validate(payload.model_dump())
        created = self.repository.create(todo)
        return TodoRead.model_validate(created)
