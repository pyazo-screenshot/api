from fastapi import FastAPI
from .db import Base, engine  # noqa: F401


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

    from .routers import shares
    app.include_router(
        shares.router,
        prefix='/shares'
    )

    from .routers import static
    app.include_router(
        static.router,
        prefix=''
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
