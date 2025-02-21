import logging

from connexion import App
from flask import Flask

from api.middleware.authn import inject_cookie_refresh
from api.middleware.env import inject_env
from api.middleware.error_handlers import error_handler_middleware
from api.middleware.mongo import inject_mongo
from api.utils.encoders import JSONEncoder

_LOGGER = logging.getLogger(__name__)


def inject_middleware(connexion_app: App, config: dict = None):
    app: Flask = connexion_app.app

    inject_env(app, config)
    inject_mongo(app)
    inject_cookie_refresh(connexion_app)

    app.json_encoder = JSONEncoder

    app.config["MAX_CONTENT_LENGTH"] = app.config["env"]["MAX_CONTENT_LENGTH"]

    _LOGGER.debug("api.middleware pre-config complete")
    connexion_app.add_error_handler(Exception, error_handler_middleware)
    return app
