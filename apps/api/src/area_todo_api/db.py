from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from area_todo_api.config import settings

engine = create_engine(settings.database_url, echo=settings.debug)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
