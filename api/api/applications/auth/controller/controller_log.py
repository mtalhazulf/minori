from datetime import date, datetime, timedelta

import pytz
from bson import ObjectId
from flask import jsonify

from api.applications.auth.helper.user import get_user
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo
from api.utils.session import get_current_user


def auth_log_post(body):
    db = get_mongo().cx.get_default_database()
    id = ObjectId()
    body["_id"] = id
    body["operator"] = ObjectId(get_current_user().uid)
    body["hour"] = datetime.now(pytz.timezone("Europe/Rome"))
    db["log"].update_one({"_id": id}, {"$set": body}, upsert=True)
    return jsonify({"success": True})


def auth_log_get():
    db = get_mongo().cx.get_default_database()
    today = datetime.combine(date.today(), datetime.min.time())
    tomorrow = today + timedelta(1)
    logs = list(
        db["log"].find(
            {
                "$query": {"hour": {"$gte": today, "$lte": tomorrow}},
                "$orderby": {"hour": -1},
            }
        )
    )
    for i, log in enumerate(logs):
        log["hour"] = log["hour"].strftime("%H:%M")
        operator = get_user(db, log["operator"])
        if (operator["type"] == "admin" or operator["type"] == "superadmin") and get_current_user().usertype == "user":
            log["isAuthorized"] = False
        if operator:
            log["operator"] = operator
        else:
            log["operator"] = "Admin"
    logs = list(filter(lambda item: "isAuthorized" not in item, logs))
    return jsonify_mongo(logs)
