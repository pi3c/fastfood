from fastapi import FastAPI


async def generate_test_data():
    """
    Создание БД и наполнение ее данными
    """
    pass


def create_app():
    """
    Создание экземпляра приложения FastAPI и врзврат его
    """
    app = FastAPI()

    return app
