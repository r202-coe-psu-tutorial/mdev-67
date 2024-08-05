from fastapi import FastAPI

from . import models

from . import routers


def create_app():
    app = FastAPI()

    models.init_db()

    routers.init_router(app)

    return app
