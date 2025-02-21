import datetime
import uuid
from functools import wraps
from typing import Callable, Optional

import jwcrypto.jwk as jwk
import python_jwt as JWT
from flask import Response, current_app, g

from api.exceptions import UserIsNotAuthorized
from api.utils.db_user import DBUser


class Session:
    def __init__(self, db_user: DBUser, auth_method: str):
        if auth_method not in ("bearer", "cookie"):
            raise ValueError(f'Invalid auth_method "${auth_method}", valid values: "bearer", "cookie"')

        self.db_user = db_user
        self.auth_method = auth_method

    def set_context(self):
        g.session = self

    @staticmethod
    def get_context():
        return getattr(g, "session", None)

    def serialize(self, ttl: int = None):
        ttl = ttl or current_app.config["env"]["AUTH"]["TOKEN_TTL" if self.auth_method == "bearer" else "COOKIE_TTL"]
        return self.serialize_session(ttl, db_user=self.db_user)

    @staticmethod
    def serialize_session(ttl: int, db_user: DBUser = None, session: dict = None) -> str:
        _jwk = jwk.JWK.from_password(current_app.config["env"]["JWT_SECRET"])
        session = session or {}
        if db_user:
            session["db_user"] = db_user.serialize()
        return JWT.generate_jwt(
            session,
            priv_key=_jwk,
            algorithm="HS512",
            lifetime=datetime.timedelta(hours=ttl),
        )

    @classmethod
    def deserialize(cls, jwt, auth_method: str) -> "Session":
        raw_session = cls.deserialize_session(jwt)
        db_user = None
        if "db_user" in raw_session:
            db_user = DBUser.unserialize(raw_session["db_user"])
        return cls(
            db_user=db_user,
            auth_method=auth_method,
        )

    @staticmethod
    def deserialize_session(jwt: str) -> dict:
        _jwk = jwk.JWK.from_password(current_app.config["env"]["JWT_SECRET"])
        header, body = JWT.verify_jwt(jwt, _jwk, allowed_algs=["HS512"], checks_optional=True)

        return body


class CookieSession(Session):
    def __init__(self, db_user: DBUser, csrf: str = None):
        Session.__init__(self, db_user, "cookie")
        self.csrf = csrf
        self._is_cookie_setted = False

    @staticmethod
    def unset_cookie_session(response: Response):
        response.set_cookie("access_token_cookie", "", httponly=True, expires=0)

    @classmethod
    def deserialize(cls, jwt) -> "CookieSession":
        raw_session = cls.deserialize_session(jwt)

        db_user = None
        if "db_user" in raw_session:
            db_user = DBUser.unserialize(raw_session["db_user"])
        csrf = raw_session.get("csrf", None)

        return cls(db_user=db_user, csrf=csrf)

    @classmethod
    def deserialize_cookie(cls, jwt) -> "CookieSession":
        return CookieSession.deserialize(jwt)

    def serialize(self, csrf: str = None, ttl: int = None):
        ttl = ttl or current_app.config["env"]["AUTH"]["COOKIE_TTL"]
        return self.serialize_session(ttl, db_user=self.db_user, csrf=csrf)

    @staticmethod
    def serialize_session(ttl: int, db_user: DBUser = None, csrf: str = None, session: dict = None) -> str:
        session = session or {}
        if csrf:
            session["csrf"] = csrf

        return Session.serialize_session(ttl, db_user, session)

    def set_cookie_session(self, response: Response):
        if self._is_cookie_setted:
            return

        self._is_cookie_setted = True

        csrf = str(uuid.uuid4()) if current_app.config["env"]["AUTH"]["CSRF_ENABLE"] else None
        response.set_cookie(
            "access_token_cookie",
            self.serialize(csrf=csrf),
            httponly=True,
            secure=current_app.config["env"]["AUTH"]["COOKIE_SECURE"],
            max_age=current_app.config["env"]["AUTH"]["COOKIE_TTL"] * 60 * 60,
        )

        if csrf:
            response.set_cookie(
                "csrf_access_token",
                csrf,
                secure=current_app.config["env"]["AUTH"]["COOKIE_SECURE"],
                max_age=current_app.config["env"]["AUTH"]["COOKIE_TTL"] * 60 * 60,
            )


def get_current_user() -> Optional[DBUser]:
    return getattr(Session.get_context(), "db_user", None)


def authorizations_required(*authorizations: str, match_all: bool = False):
    """
    parameterizable decorator that raise an exception if current_user have not the requested authz

    :param authorizations: list of failed authz
    :param match_all: bool, if False, current_user is authorized if at least one authz match,
    else the user must have all the *authorizations authz
    :return:
    """

    def decorator(f: Callable):
        @wraps(f)
        def wrapper(*args, **kwargs):
            unauthorized = []
            for authz in authorizations:
                if not get_current_user().is_authorized(authz):
                    unauthorized += [authz]

            if match_all and unauthorized:
                raise UserIsNotAuthorized(unauthorized, match_all=match_all)
            elif not match_all and len(unauthorized) == len(authorizations):
                raise UserIsNotAuthorized(unauthorized, match_all=match_all)

            return f(*args, **kwargs)

        return wrapper

    return decorator
