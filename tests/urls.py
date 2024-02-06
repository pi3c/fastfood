from fastfood.app import create_app

app = create_app()


def reverse(loc: str, **kwargs) -> str:

    url = app.url_path_for(loc, **kwargs)
    return url
