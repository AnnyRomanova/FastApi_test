from pydantic_settings import BaseSettings


# класс для определения параметров подключения к бд
class DatabaseConfig(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

# метод возвращает строку подключения
    def make_url(self, driver: str) -> str:
        return f"{driver}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

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
        env_file = ".env"  # Путь к файлу .env
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings(DB=DatabaseConfig())
