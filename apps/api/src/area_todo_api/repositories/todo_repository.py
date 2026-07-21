from sqlmodel import Session, select

from area_todo_api.models.todo import Todo


class TodoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[Todo]:
        statement = select(Todo).order_by(Todo.created_at.desc())
        return list(self.session.exec(statement).all())

    def create(self, todo: Todo) -> Todo:
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo
