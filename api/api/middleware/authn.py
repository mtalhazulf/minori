from connexion import App
from flask import request
from python_jwt import _JWTError
from werkzeug.exceptions import Unauthorized

from api.utils.session import CookieSession, Session


def authn_bearer(api_key, required_scopes):
    """
    connexion handler for Bearer authn
    """
    if not api_key:
        return None
    try:
        session = Session.deserialize(api_key, "bearer")
        session.set_context()
    except _JWTError as e:
        if str(e) == "expired":
            raise Unauthorized("Token expired")
    except Exception:
        raise Unauthorized()
    return {"uid": api_key}


def authn_cookie(cookie, required_scopes):
    """
    connexion handler for Bearer authn
    """
    if not cookie:
        return None
    try:
        session = CookieSession.deserialize_cookie(cookie)
        session.set_context()
        csrf_guard()
    except Exception:
        raise Unauthorized()
    return {"uid": cookie}


def csrf_guard():
    # CSRF check only in cookie
    if not isinstance(session := Session.get_context(), CookieSession):
        return None

    # exclude "safe" methods
    if request.method in ["GET", "OPTIONS"]:
        return None

    # if CSRF is None, then CSRF is disabled, so ignore the check
    if session.csrf and request.headers["X-CSRF-TOKEN"] != session.csrf:
        raise Unauthorized("Failed CSRF security check")

    return None


def inject_cookie_refresh(app: App):
    @app.app.after_request
    def refresh_cookie(response):
        if isinstance(session := Session.get_context(), CookieSession):
            session.set_cookie_session(response)

        return response
