import falcon
from falcon import App

from gcmanager.dependencies import build_dependency_container
from gcmanager.routes import make_router


def create_app() -> falcon.App:
    container = build_dependency_container()
    router = make_router(container)
    app = App(router=router)
    return app
