from datetime import datetime

from bson import ObjectId

from api.middleware.mongo import get_mongo


def stamping_config_operation_post(body):
    if "status" in body:
        db = get_mongo().cx.get_default_database()
        datetime.now()
        id = ObjectId()
        body["_id"] = id
        body["creation_date"] = datetime.now()
        updated = db["log"].update_one({"_id": id}, {"$set": body}, upsert=True)
        if updated.matched_count < 0:
            return {"status": -1}
    return {"status": 0}
