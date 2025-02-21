import logging.config
from pathlib import Path

import connexion
from dotenv import load_dotenv
from flask_cors import CORS

from .middleware import inject_middleware
from .utils.connexion_utils import CamelCaseRestyResolver

logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "class": "logging.Formatter",
                "format": "%(asctime)sZ [%(levelname)s] [tid:%(thread)d] %(name)s: %(message)s ",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            }
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "default", "stream": "ext://sys.stdout"}
        },
        "root": {"handlers": ["console"], "level": "INFO"},
        "loggers": {"gunicorn": {"level": "INFO"}, "api": {"level": "INFO"}},
    }
)


def create_app():
    openapi_path = Path(__file__).parent / "openapi.yaml"
    load_dotenv()

    app = connexion.App(__name__, specification_dir=openapi_path.parent)

    inject_middleware(app)

    app.add_api(
        openapi_path.name,
        resolver=CamelCaseRestyResolver("api"),
        pythonic_params=False,
        strict_validation=app.app.config["env"]["VALIDATE_REQUEST"],
        validate_responses=app.app.config["env"]["DEBUG"]["VALIDATE_RESPONSE"],
        options={"swagger_url": "/docs"},
    )
    # CORS(app.app)
    # CORS(app.app, resources={r"/*": {"origins": "*"}})
    CORS(app.app, supports_credentials=True)

    return app
