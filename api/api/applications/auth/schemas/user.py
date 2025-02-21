from schema import And, Optional, Schema, Use

from api.utils.db_user import DBUser

user_post_schema = Schema(
    {
        "name": And(str, lambda s: len(s) > 0),
        "surname": And(str, lambda s: len(s) > 0),
        "subscriber": And(str, lambda s: len(s) > 0),
        "password": And(str, lambda s: len(s) >= 8, Use(DBUser.hash_password)),
        "email": And(str, lambda s: len(s) > 0),
        "username": And(str, lambda s: len(s) > 0, Use(lambda x: x.lower())),
        "status": str,
        "type": str,
        "role": str,
        "fiscal_code": str,
        Optional("hourly_cost"): And(Use(float), lambda x: x > 0),
    }
)

change_password_schema = Schema(
    {
        "password": And(str, lambda s: len(s) >= 8, Use(DBUser.hash_password)),
        "new_password": And(str, lambda s: len(s) >= 8, Use(DBUser.hash_password)),
    }
)

change_password_arg_schema = Schema(
    {
        "password": And(str, lambda s: len(s) >= 8, Use(DBUser.hash_password)),
    }
)
