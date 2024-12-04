from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str


def get_settings() -> Settings:
    return Settings()
