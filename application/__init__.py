from fastapi import FastAPI
from application.db import Base, engine


def init_routers(app: FastAPI):
    from .routers import auth
    app.include_router(
        auth.router,
        prefix='/auth'
    )

    from .routers import images
    app.include_router(
        images.router,
        prefix='/images'
    )


def init_middlewares(app: FastAPI):
    from fastapi.middleware.cors import CORSMiddleware

    origins = ['*']

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def create_app() -> FastAPI:
    app = FastAPI()
    init_routers(app)
    init_middlewares(app)

    return app
