import os

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
    def DATABASE_URL_asyncpg(self) -> str:
        """
        Возвращает строку подключения к БД необходимую для SQLAlchemy
        """
        # Проверяем, в DOCKER или нет

        file_path = '/usr/src/RUN_IN_DOCKER'
        if os.path.exists(file_path):
            return (
                'postgresql+asyncpg://'
                f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
                f'@db:{self.DB_PORT}/{self.POSTGRES_DB}'
            )

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
        file_path = '/usr/src/RUN_IN_DOCKER'
        if os.path.exists(file_path):
            return (
                'postgresql+asyncpg://'
                f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
                f'@db:{self.DB_PORT}/{self.POSTGRES_DB_TEST}'
            )

        return (
            'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB_TEST}'
        )

    @property
    def REDIS_URL(self):
        file_path = '/usr/src/RUN_IN_DOCKER'
        if os.path.exists(file_path):
            return 'redis://redis:6379/0'

        return self.REDIS_DB

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
