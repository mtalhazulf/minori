import json
import logging

from bson.errors import InvalidId
from dateutil.parser import ParserError as DateParserError
from flask import Response
from werkzeug.exceptions import HTTPException, InternalServerError

_LOGGER = logging.getLogger(__name__)

DEFAULT_ERROR_MIMETYPE = "application/problem+json"


# ERROR HANDLER MIDDLEWARES
def http_exception_error_handler(error: HTTPException):
    if error.code >= 500:
        _LOGGER.error("Server error", exc_info=error)
    else:
        _LOGGER.debug("Error", exc_info=error)

    return Response(
        response=json.dumps({"description": error.description, "error": error.name}),
        status=error.code,
        mimetype=DEFAULT_ERROR_MIMETYPE,
    )


def error_handler_middleware(error: Exception):
    if isinstance(error, HTTPException):
        return http_exception_error_handler(error)

    # misc client errro exceptions
    if isinstance(error, DateParserError):
        return Response(
            response=json.dumps(
                {
                    "description": "Formato delle date non valido",
                    "error": "DateParserError",
                }
            ),
            status=400,
            mimetype=DEFAULT_ERROR_MIMETYPE,
        )

    if isinstance(error, InvalidId):
        return Response(
            response=json.dumps({"description": "Id non valido", "error": "InvalidId"}),
            status=400,
            mimetype=DEFAULT_ERROR_MIMETYPE,
        )

    # if the exception hasn't been managed till now, return a 500 internal error
    _LOGGER.exception(f"Unmanaged exception {error.__class__.__name__}, returning 500", exc_info=error)
    return http_exception_error_handler(InternalServerError())
