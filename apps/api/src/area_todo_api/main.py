from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from area_todo_api.config import settings
from area_todo_api.controllers.health import router as health_router
from area_todo_api.controllers.todos import router as todos_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(todos_router)

    return app


app = create_app()
