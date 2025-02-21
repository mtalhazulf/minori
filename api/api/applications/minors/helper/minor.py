from datetime import datetime

from bson import ObjectId
from flask import jsonify
from werkzeug.exceptions import BadRequest

from api.applications.adults.helper.adult import get_adult
from api.applications.auth.helper.user import get_user
from api.applications.minors.helper.attendance import update_attendances
from api.applications.settings.helper.settings import get_resource
from api.utils.log import Log


def get_minor(db, id):
    return db["children"].find_one({"_id": id})


def update_minor(db, id, now):
    updated = db["children"].update_one(
        {
            "_id": ObjectId(id),
        },
        {"$set": {"status": "disabled", "deactivation_date": now}},
    )
    if updated.matched_count > 0:
        Log(
            application="minors",
            subject="minor",
            action="disable minor",
            resource=ObjectId(id),
        ).store_log()
        return jsonify({"success": True})
    else:
        raise BadRequest("Minore non disabilitato")


def remove_attendance(db, id):
    db["minorAttendance"].delete_one({"_id": ObjectId(id)})


def edit_minor(db, id, body):
    if "fiscal_code" in body and db["children"].find_one(
        {
            "$and": [
                {"fiscal_code": body["fiscal_code"]},
                {"_id": {"$ne": ObjectId(id)}, "fiscal_code": {"$exists": True}},
                {"$or": [{"status": "enabled"}, {"status": {"$exists": False}}]},
            ]
        }
    ):
        return {"success": False, "msg": "Il codice fiscale inserito è già in uso"}
    elif db["children"].find_one(
        {
            "name": body["name"],
            "surname": body["surname"],
            "_id": {"$ne": ObjectId(id)},
            "$or": [{"status": "enabled"}, {"status": {"$exists": False}}],
        }
    ):
        return {
            "success": False,
            "msg": "Nome e cognome già in uso, si prega di specificare il codice fiscale se si vuole ugualmente "
            "inserire il minore.",
        }
    else:
        update = db["children"].update_one(
            {
                "_id": ObjectId(id),
            },
            {"$set": body},
        )
        if update.matched_count > 0:
            update_attendances(db, id)
            Log(
                application="minors",
                subject="minor",
                action="edit minor",
                resource=ObjectId(id),
            ).store_log()
            return {"success": True}
        else:
            raise BadRequest("Minore non modificato")


def remove_empty_attributes(obj):
    if isinstance(obj, dict):
        cleaned_dict = {k: remove_empty_attributes(v) for k, v in obj.items() if v != ""}
        return {
            k: v for k, v in cleaned_dict.items() if v or isinstance(v, bool)
        }  # Ensure boolean False is not removed
    elif isinstance(obj, list):
        return [remove_empty_attributes(v) for v in obj if v != ""]
    else:
        return obj


def fetch_tasks_between_date_range(db, data):
    start_date = data["start_date"]
    end_date = data["end_date"]
    data["start_date"] = datetime.strptime(data["start_date"], "%Y-%m-%d")
    data["end_date"] = datetime.strptime(data["end_date"], "%Y-%m-%d")

    start_date = datetime.combine(data["start_date"].date(), datetime.min.time())
    end_date = datetime.combine(data["end_date"].date(), datetime.min.time())

    filter_query = {"start": {"$gte": start_date, "$lte": end_date}, "status": "done", "minor": ObjectId(data["id"])}

    events = list(db["tasks"].find(filter_query))

    for event in events:
        event["start"] = event["start"].strftime("%Y-%m-%d %H:%M:%S")
        if "minor" in event:
            minor = get_minor(db, event["minor"])
            event["minor"] = minor if minor else "Minore"
        if "adult" in event:
            adult = get_adult(db, event["adult"])
            event["adult"] = adult if adult else "Adulto"
        if "resource" in event:
            resource_module, resource_type = get_resource(db, event["resource"]["module"], event["resource"]["type"])
            event["resource"]["module"] = resource_module if resource_module else "Modulo HCCP"
            event["resource"]["type"] = resource_type if resource_type else ""
        if "operator" in event:
            operator = get_user(db, event["operator"])
            event["operator"] = operator if operator else "User"

    return events
