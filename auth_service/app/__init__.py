from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.v1.endpoint import router, UserRouter
from .core.config import ConfigAPP
from .db.connections import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняемый при запуске
    await init_db()
    yield  # Переход к следующей части (запуск приложения)

    # Код, выполняемый при завершении
    print("Shutting down application")


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan,
                  title=ConfigAPP.APP_TITLE,
                  description=ConfigAPP.APP_DESCRIPTION,
                  version=ConfigAPP.APP_VERSION,
                  openapi_tags=ConfigAPP.OPENAPI_TAGS
                  )

    user_router = UserRouter().router
    app.include_router(user_router, prefix='/auth')

    @app.get('/', tags=["Other"], description='Check health')
    async def health_check():
        return {"Hello": "World auth"}

    return app
