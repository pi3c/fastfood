from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    POSTGRES_DB: str = "fastfood_db"
    POSTGRES_PASSWORD: str = "test"
    POSTGRES_USER: str = "testuser"
    POSTGRES_DB_TEST: str = "fastfood_db_test"

    @property
    def DATABASE_URL_asyncpg(self):
        """
        Возвращает строку подключения к БД необходимую для SQLAlchemy
        """
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def TESTDATABASE_URL_asyncpg(self):
        """
        Возвращает строку подключения к БД необходимую для SQLAlchemy
        """
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB_TEST}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
