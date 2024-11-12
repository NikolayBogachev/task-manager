
import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str
    URL_DB: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    URL: str
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        extra = "forbid"


config = Settings()
