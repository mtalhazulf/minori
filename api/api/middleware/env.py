from os import environ

from flask import Flask
from schema import And, Optional, Or, Schema, Use

_BOOL_VALIDATOR = Or(And(Use(int), Use(bool)), Use(bool))

_ENV_SCHEMAS = [
    Schema(
        {
            "MONGO_URI": str,
            "JWT_SECRET": str,
            Optional("CONNEXION_VALIDATE_REQUEST", default=True): _BOOL_VALIDATOR,
            Optional("CONNEXION_VALIDATE_RESPONSE", default=False): _BOOL_VALIDATOR,
            Optional("CSRF_ENABLE", default=False): _BOOL_VALIDATOR,
            # max document size, 256MB
            Optional("MAX_CONTENT_LENGTH", default=268435456): Use(int),
            # cookie max_age / JWT TTL (for cookie), in hours
            Optional("AUTH_COOKIE_TTL", default=24): Use(float),
            # enable secure flag in cookie (default true, disable only for debug purpose only)
            Optional("BACH_AUTH_COOKIE_SECURE", default=True): _BOOL_VALIDATOR,
            # JWT TTL for /auth/access-token and /auth/refresh-token, in hours
            Optional("AUTH_TOKEN_TTL", default=24): Use(float),
        }
    )
]


def _get_envs_keys(schema: Schema):
    env_schema_key = []
    if not hasattr(schema.schema, "keys"):
        keys = []
        for arg in schema.schema.args:
            keys += _get_envs_keys(arg)
        return keys
    for e in schema.schema.keys():
        if isinstance(e, str):
            env_schema_key += [e]
        elif isinstance(e, Optional):
            env_schema_key += [e.schema]
    return env_schema_key


def _validate_schema(schema: Schema, source: dict) -> dict:
    keys = _get_envs_keys(schema)
    envs = {}
    for env in keys:
        if source.get(env) is not None:
            envs[env] = source.get(env)

    return schema.validate(envs)


def _format_envs(validated_envs: dict):
    return {
        "MONGO_URI": validated_envs.get("MONGO_URI"),
        "JWT_SECRET": validated_envs.get("JWT_SECRET"),
        "MAX_CONTENT_LENGTH": validated_envs.get("MAX_CONTENT_LENGTH"),
        "VALIDATE_REQUEST": validated_envs.get("CONNEXION_VALIDATE_REQUEST"),
        "DEBUG": {"VALIDATE_RESPONSE": validated_envs.get("CONNEXION_VALIDATE_RESPONSE")},
        "AUTH": {
            "CSRF_ENABLE": validated_envs.get("CSRF_ENABLE"),
            "COOKIE_SECURE": validated_envs.get("AUTH_COOKIE_SECURE"),
            "COOKIE_TTL": validated_envs.get("AUTH_COOKIE_TTL"),
            "TOKEN_TTL": validated_envs.get("AUTH_TOKEN_TTL"),
        },
    }


def load_env(source: dict = None):
    source = source or environ
    validated_env_list = [_validate_schema(schema, source) for schema in _ENV_SCHEMAS]
    validated_envs = {}
    for envs in validated_env_list:
        validated_envs.update(**envs)
    return _format_envs(validated_envs)


def inject_env(app: Flask, source: dict = None):
    app.config["env"] = load_env(source)
