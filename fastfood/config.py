from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = ''
    DB_PORT: int = 5432
    POSTGRES_DB: str = ''
    POSTGRES_PASSWORD: str = ''
    POSTGRES_USER: str = ''
    POSTGRES_DB_TEST: str = ''
    REDIS_DB: str = ''

    @property
    def DATABASE_URL_asyncpg(self):
        """
        Возвращает строку подключения к БД необходимую для SQLAlchemy
        """
        return (
            'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'
        )

    @property
    def TESTDATABASE_URL_asyncpg(self):
        """
        Возвращает строку подключения к БД необходимую для SQLAlchemy
        """
        return (
            'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB_TEST}'
        )

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
