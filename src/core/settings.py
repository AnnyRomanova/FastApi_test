from pydantic_settings import BaseSettings


# класс для определения параметров подключения к бд
class DatabaseConfig(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    DB: str

    # метод возвращает строку подключения
    def make_url(self, driver: str) -> str:
        return f"{driver}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"

    # для ассинхронных запросов: asyncpg вместо psycopg2
    @property
    def asyncpg_url(self) -> str:
        return self.make_url(driver="postgresql+asyncpg")

    # для синхронного подключения
    @property
    def postgresql_url(self) -> str:
        return self.make_url(driver="postgresql")


class Settings(BaseSettings):
    APP_NAME: str
    DB: DatabaseConfig

    class Config:
        case_sensitive = True
        env_nested_delimiter = "__"


def get_settings() -> Settings:
    return Settings()
