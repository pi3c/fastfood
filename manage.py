import sys

import uvicorn


def run_app():
    """
    Запуск
    """
    uvicorn.run(
        app="fastfood.app:create_app",
        reload=True,
        factory=True,
    )


if __name__ == "__main__":
    if "filldb" in sys.argv:
        """Наполнение БД демонстрационными данными"""
        pass

    if "--run-server" in sys.argv:
        run_app()
