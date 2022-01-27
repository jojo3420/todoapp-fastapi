from functools import lru_cache
from pydantic import BaseSettings
from pydantic.types import SecretStr


class Settings(BaseSettings):
    """환경변수"""

    # DB Connection
    DB_USERNAME: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: str
    DB_SCHEMA: str

    # DB POOL
    QUERY_DEBUG_MODE: bool
    DB_POOL_RECYCLE: int
    DB_POOL_SIZE: int
    DB_MAX_POOL_OVERFLOW: int

    class Config:
        env_file = ".env"
        env_file_encoding = "UTF-8"


# settings 은 앱에서 자주사용하므로 캐싱을 한다.
# Least Recently-Used cache decorator
@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
