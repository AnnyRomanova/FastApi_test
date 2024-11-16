from pydantic import Field
from pydantic_settings import BaseSettings

import os

app_name = os.getenv("APP_NAME")

class Settings(BaseSettings):
    app_name: str = Field("Magazine articles", env="APP_NAME")


settings = Settings()


