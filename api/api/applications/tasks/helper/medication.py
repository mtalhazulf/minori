from datetime import datetime

from bson import ObjectId
from werkzeug.exceptions import BadRequest


def update_medication(db, id, body):
    body["expiration_date"] = datetime.combine(
        datetime.strptime(body["expiration_date"], "%d/%m/%Y"), datetime.min.time()
    )
    updated = db["medication"].update_one(
        {
            "_id": ObjectId(id),
        },
        {"$set": body},
    )
    if updated.matched_count > 0:
        return {"success": True}
    else:
        raise BadRequest("Farmaco non modificato")


def queryParams(data):
    query = {}
    for field in data:
        if isinstance(data[field], str) and len(data[field]) > 0:
            query[field] = {"$regex": data[field]}
        if isinstance(data[field], int) and data[field] > 0:
            query[field] = data[field]
        if isinstance(data[field], datetime):
            query[field] = {"$gt": data[field]}
        if isinstance(data[field], ObjectId):
            query[field] = data[field]
        if isinstance(data[field], bool):
            query[field] = data[field]
    return query
