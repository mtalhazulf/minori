from datetime import datetime, timedelta

from bson import ObjectId
from flask import jsonify, request

from api.applications.events.helper.event import get_events, get_tasks
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo


def events_get():
    db = get_mongo().cx.get_default_database()
    if request.args and "date" in request.args.to_dict():
        return jsonify_mongo(get_events(db, request.args.to_dict()))
    if request.args and "today_date" in request.args.to_dict():
        return jsonify_mongo(get_tasks(db, request.args.to_dict()))


def events_expiring_get():
    db = get_mongo().cx.get_default_database()
    first = datetime.combine(datetime.now(), datetime.min.time())
    last = first + timedelta(days=15)
    events = list(db["events"].find({"start": {"$gte": first, "$lte": last}}))
    return jsonify(count=len(events), expiring=True if len(events) > 0 else False)


def events_post(body):
    db = get_mongo().cx.get_default_database()
    _id = ObjectId()
    today = datetime.now()
    if "minor" in body and body["minor"] is not None:
        body["minor"] = ObjectId(body["minor"])
    body["start"] = datetime.strptime(body["start"], "%d/%m/%Y %H:%M")
    db["events"].update_one(
        {"_id": ObjectId(_id)},
        {"$set": {**body, "creation_date": today, "selected": False}},
        upsert=True,
    )
    return {"success": True}


def events_arg_delete(arg):
    db = get_mongo().cx.get_default_database()
    db["events"].delete_one({"_id": ObjectId(arg)})
    return {"success": True}
