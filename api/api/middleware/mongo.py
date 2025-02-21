import logging

from flask import Flask
from flask_pymongo import PyMongo

_LOGGER = logging.getLogger(__name__)

__mongo: PyMongo = None


def inject_mongo(app: Flask):
    global __mongo
    app.config["MONGO_URI"] = app.config["env"]["MONGO_URI"]

    _LOGGER.debug("Init mongo connection...")
    __mongo = PyMongo(app)


def get_mongo():
    global __mongo
    return __mongo
