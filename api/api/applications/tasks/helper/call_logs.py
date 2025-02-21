from datetime import datetime

from bson import ObjectId
from werkzeug.exceptions import BadRequest


def update_call_log(db, id, body):
    body["date"] = datetime.strptime(body["date"], "%d/%m/%Y %H:%M:%S")
    updated = db["callLogs"].update_one(
        {
            "_id": ObjectId(id),
        },
        {"$set": body},
    )
    if updated.matched_count > 0:
        return {"success": True}
    else:
        raise BadRequest("Telefonata non modificata")
