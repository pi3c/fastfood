import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Конфиг PostgreSql
    POSTGRES_HOST: str = ''
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ''
    POSTGRES_PASSWORD: str = ''
    POSTGRES_USER: str = ''
    POSTGRES_DB_TEST: str = ''
    # Конфиг Redis
    REDIS_HOST: str = ''
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

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
                f'@db:5432/{self.POSTGRES_DB}'
            )

        return (
            'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
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
                f'@db:5432/{self.POSTGRES_DB_TEST}'
            )

        return (
            'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB_TEST}'
        )

    @property
    def REDIS_URL(self):
        """
        Возвращает строку подключения к REDIS
        """
        file_path = '/usr/src/RUN_IN_DOCKER'
        if os.path.exists(file_path):
            return 'redis://redis:6379/0'

        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'

    @property
    def REBBITMQ_URL(self):
        """
        Возвращает строку подключения к REBBITMQ
        """
        file_path = '/usr/src/RUN_IN_DOCKER'
        if os.path.exists(file_path):
            return 'amqp://guest:guest@rabbitmq'

        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
