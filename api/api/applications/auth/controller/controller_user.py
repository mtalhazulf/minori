import secrets
import string
from datetime import datetime

from bson import ObjectId
from flask import jsonify, request
from werkzeug.exceptions import BadRequest

from api.applications.auth.helper.user import (
    get_user,
    get_user_by_username,
    remove_operator_badge,
    update_operator_badge,
)
from api.applications.auth.schemas.user import (
    change_password_arg_schema,
    change_password_schema,
    user_post_schema,
)
from api.applications.settings.helper.settings import get_element
from api.applications.shifts.helper.shift import get_shifts_with_cost
from api.exceptions import InvalidSchemaException
from api.middleware.mongo import get_mongo
from api.utils.jsonify_mongo import jsonify_mongo
from api.utils.log import Log
from api.utils.session import get_current_user


def auth_user_arg_get(arg):
    db = get_mongo().cx.get_default_database()
    return jsonify_mongo(get_user(db, arg))


def auth_user_arg_put(arg):
    db = get_mongo().cx.get_default_database()
    now = datetime.now()
    updated = db["users"].update_one(
        {
            "_id": ObjectId(arg),
        },
        {
            "$set": {"status": "disabled", "deactivation_date": now},
            "$unset": {"badgeId": ""},
        },
    )
    if updated.matched_count > 0:
        Log(
            application="auth",
            subject="user",
            action="disable user",
            resource=ObjectId(arg),
        ).store_log()
        return jsonify({"success": True})
    else:
        raise BadRequest("Operatore non disabilitato")


def auth_user_edit_arg_put(arg, body):
    db = get_mongo().cx.get_default_database()
    if db["users"].find_one({"_id": ObjectId(arg)}):
        if db["users"].find_one(
            {
                "username": body["username"],
                "_id": {"$ne": ObjectId(arg)},
                "$or": [
                    {"status": "enabled"},
                    {"status": {"$exists": False}},
                ],
            }
        ):
            return {"success": False, "msg": "L'username inserito è già in uso"}
        elif db["users"].find_one(
            {
                "fiscal_code": body["fiscal_code"],
                "_id": {"$ne": ObjectId(arg)},
                "$or": [
                    {"status": "enabled"},
                    {"status": {"$exists": False}},
                ],
            }
        ):
            return {"success": False, "msg": "Il codice fiscale inserito è già in uso"}
        else:
            body["role"] = ObjectId(body["role"])
            update = db["users"].update_one(
                {
                    "_id": ObjectId(arg),
                },
                {"$set": body},
            )
            if update.matched_count > 0:
                Log(
                    application="auth",
                    subject="user",
                    action="edit user",
                    resource=ObjectId(arg),
                ).store_log()
                return {"success": True}
            else:
                raise BadRequest("Operatore non modificato")
    else:
        raise BadRequest("Operatore non esiste")


def auth_user_post(body):
    db = get_mongo().cx.get_default_database()
    if db["users"].find_one(
        {
            "username": body["username"],
            "$or": [
                {"status": "enabled"},
                {"status": {"$exists": False}},
            ],
        }
    ):
        return {"success": False, "msg": "L'username inserito è già in uso"}
    elif db["users"].find_one(
        {
            "fiscal_code": body["fiscal_code"],
            "$or": [
                {"status": "enabled"},
                {"status": {"$exists": False}},
            ],
        }
    ):
        return {"success": False, "msg": "Il codice fiscale inserito è già in uso"}
    else:
        alphabet = string.ascii_letters + string.digits
        while True:
            password = "".join(secrets.choice(alphabet) for i in range(10))
            if (
                any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
            ):
                break
        body["password"] = password
        body["subscriber"] = get_current_user().subscriber
        if get_user_by_username(db, body["username"]):
            return jsonify({"success": False})
        else:
            try:
                body = user_post_schema.validate(body)
            except Exception:
                raise InvalidSchemaException()
            body["role"] = ObjectId(body["role"])
            r = db["users"].insert_one(body)
            id = r.inserted_id
            if id:
                return jsonify({"success": True, "password": password})
            else:
                return jsonify({"success": False})


def auth_user_assign_post(body):
    db = get_mongo().cx.get_default_database()
    for badge in body["badge_assignment"]:
        if "badgeId" in badge and badge["badgeId"] is not None:
            update_operator_badge(db, badge["badgeId"], badge["operator"])
        else:
            remove_operator_badge(db, badge["operator"])
    return jsonify({"success": True})


def auth_user_subscribers_get():
    db = get_mongo().cx.get_default_database()
    return jsonify_mongo(db["users"].find({"type": "admin"}))


# def auth_user_operators_get():
#     db = get_mongo().cx.get_default_database()
#     try:
#         query = {"type": "user"}
#         if len(request.args) > 0:
#             if request.args.get("status"):
#                 query["status"] = request.args.get("status")
#         users = list(db["users"].find(query).sort("name", 1))

#         for user in users:
#             monthly_hours = get_hours_worked(db, user["_id"])
#             if "role" in user and bson.objectid.ObjectId.is_valid(user["role"]):
#                 user["role"] = get_element(db, "user", "roles", user["role"])
#                 if "hourly_cost" in user:
#                     user["monthly_cost"] = round(monthly_hours * float(user["hourly_cost"]), 2)
#                 else:
#                     user["monthly_cost"] = round(monthly_hours * user["role"]["average_hour_cost"], 2)
#             if "deactivation_date" in user:
#                 user["deactivation_date"] = user["deactivation_date"].strftime("%Y-%m-%d %H:%M")
#         return jsonify_mongo(users)
#     except Exception as e:
#         print(f"An error occurred: {e}")


def auth_user_operators_get():
    db = get_mongo().cx.get_default_database()
    try:
        query = {"type": "user"}
        if len(request.args) > 0:
            if request.args.get("status"):
                query["status"] = request.args.get("status")
        users = list(db["users"].find(query).sort("name", 1))

        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        shift_data = get_shifts_with_cost(db, {"date": formatted_date})

        operator_costs = {op["operator_id"]: op for op in shift_data["operator_costs"]}

        for user in users:
            user_id = str(user["_id"])
            if user_id in operator_costs:
                user["monthly_hours"] = operator_costs[user_id]["total_hours"]
                user["monthly_cost"] = operator_costs[user_id]["total_cost"]
            else:
                user["monthly_hours"] = 0
                user["monthly_cost"] = 0

            if "role" in user and ObjectId.is_valid(user["role"]):
                user["role"] = get_element(db, "user", "roles", user["role"])

            if "deactivation_date" in user:
                user["deactivation_date"] = user["deactivation_date"].strftime("%Y-%m-%d %H:%M")

        return jsonify_mongo(users)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


def auth_user_change_password_put(body):
    db = get_mongo().cx.get_default_database()
    try:
        data = change_password_schema.validate(body)
    except Exception:
        raise InvalidSchemaException()
    user = db["users"].find_one({"_id": ObjectId(get_current_user().uid), "password": data["password"]})
    if user:
        updated = db["users"].update_one(
            {
                "_id": ObjectId(get_current_user().uid),
            },
            {"$set": {"password": data["new_password"]}},
        )
        if updated.matched_count > 0:
            Log(
                application="auth",
                subject="user",
                action="change password",
                resource=ObjectId(get_current_user().uid),
            ).store_log()
            return jsonify({"success": True})
        else:
            raise BadRequest("Password non modificata")
    raise BadRequest("Password inserita sbagliata")


def auth_user_change_password_arg_put(id, body):
    db = get_mongo().cx.get_default_database()
    try:
        data = change_password_arg_schema.validate(body)
    except Exception:
        raise InvalidSchemaException()
    updated = db["users"].update_one(
        {
            "_id": ObjectId(id),
        },
        {"$set": {"password": data["password"]}},
    )
    if updated.matched_count > 0:
        Log(
            application="auth",
            subject="user",
            action="change password",
            resource=ObjectId(id),
        ).store_log()
        return jsonify({"success": True, "password": body["password"]})
    else:
        raise BadRequest("Password non modificata")
