from bson import ObjectId
from flask import jsonify
from werkzeug.exceptions import BadRequest

from api.applications.adults.helper.attendance import update_attendances
from api.utils.log import Log


def get_adult(db, id):
    return db["adults"].find_one({"_id": id})


def update_adult(db, id, now):
    updated = db["adults"].update_one(
        {
            "_id": ObjectId(id),
        },
        {"$set": {"status": "disabled", "deactivation_date": now}},
    )
    if updated.matched_count > 0:
        Log(
            application="adults",
            subject="adult",
            action="disable adult",
            resource=ObjectId(id),
        ).store_log()
        return jsonify({"success": True})
    else:
        raise BadRequest("Adulto non disabilitato")


def remove_attendance(db, id):
    db["adultAttendance"].delete_one({"_id": ObjectId(id)})


def edit_adult(db, id, body):
    if "fiscal_code" in body and db["adults"].find_one(
        {
            "$and": [
                {"fiscal_code": body["fiscal_code"]},
                {"_id": {"$ne": ObjectId(id)}, "fiscal_code": {"$exists": True}},
                {"$or": [{"status": "enabled"}, {"status": {"$exists": False}}]},
            ]
        }
    ):
        return {"success": False, "msg": "Il codice fiscale inserito è già in uso"}
    elif db["adults"].find_one(
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
            "inserire il adulte.",
        }
    else:
        update = db["adults"].update_one(
            {
                "_id": ObjectId(id),
            },
            {"$set": body},
        )
        if update.matched_count > 0:
            update_attendances(db, id)
            Log(
                application="adults",
                subject="adult",
                action="edit adult",
                resource=ObjectId(id),
            ).store_log()
            return {"success": True}
        else:
            raise BadRequest("Adulto non modificato")
