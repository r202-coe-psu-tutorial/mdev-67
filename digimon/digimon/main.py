from fastapi import FastAPI

from . import config
from . import models

from . import routers


def create_app(settings=None):
    if not settings:
        settings = config.get_settings()

    app = FastAPI()

    models.init_db(settings)

    routers.init_router(app)
    return app
