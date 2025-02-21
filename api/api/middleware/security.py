from flask import request
from werkzeug.exceptions import MethodNotAllowed

WHITELISTED_HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]


def whitelist_http_methods():
    if request.method not in WHITELISTED_HTTP_METHODS:
        raise MethodNotAllowed()


def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response
