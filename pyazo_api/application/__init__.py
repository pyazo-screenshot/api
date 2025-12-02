from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import lifespan
from .routers import auth, images


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://app.pyazo.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(images.router, prefix="/images", tags=["images"])

    return app
