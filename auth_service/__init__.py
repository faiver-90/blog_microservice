from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import ConfigAPP
from app import init_db


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

    # register_routers(app)

    @app.get('/', tags=["Other"], description='Check health')
    async def health_check():
        return {"Hello": "World"}

    return app
