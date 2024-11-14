from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field("Magazine articles", env="APP_NAME")


settings = Settings()


