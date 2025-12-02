from functools import lru_cache
from typing import override

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: str = "production"

    postgres_user: str = "pyazo"
    postgres_password: str = ""
    postgres_db: str = "pyazo"
    postgres_host: str = "localhost"

    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"

    block_register: bool = True
    images_path: str = "/images"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}/{self.postgres_db}"

    @property
    def is_development(self) -> bool:
        return self.env == "development"

    @property
    def is_testing(self) -> bool:
        return self.env == "testing"


@lru_cache
def get_settings() -> Settings:
    return Settings()
