from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    POSTGRES_DB: str = "fastfod_db"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_USER: str = "postgres"

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
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}_test"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
