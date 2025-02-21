from datetime import date, datetime

from bson import ObjectId

from api.middleware.mongo import get_mongo


def get_minor_attendance(db, id, date):
    attendance = list(db["minorAttendance"].find({"_id": id, "date": date}))
    return True if len(attendance) > 0 else False


def get_minor_attendances(db, date):
    attendance = list(db["minorAttendance"].find({"date": date}))
    return True if len(attendance) > 0 else False


def add_minor_attendance(data):
    db = get_mongo().cx.get_default_database()
    att_date = datetime.combine(date.today(), datetime.min.time())
    if get_minor_attendance(db, ObjectId(data["_id"]["$oid"]), att_date):
        db["minorAttendance"].update_one(
            {"_id": ObjectId(data["_id"]["$oid"])},
            {"$set": {"isPresent": data["isPresent"]}},
        )
    else:
        id = ObjectId()
        data["minorId"] = ObjectId(data["_id"]["$oid"])
        data["_id"] = id
        data["date"] = att_date
        data["creation_date"] = att_date
        if "creation_user" in data:
            data["creation_user"] = ObjectId(data["creation_user"]["$oid"])
        db["minorAttendance"].update_one({"_id": id}, {"$set": data}, upsert=True)


def update_attendances(db, id):
    minor = db["children"].find_one({"_id": ObjectId(id)})
    if minor:
        db["minorAttendance"].update(
            {
                "minorId": ObjectId(id),
            },
            {"$set": {"name": minor["name"], "surname": minor["surname"]}},
        )


def check_attendance(db, id, body):
    att_date = datetime.combine(date.today(), datetime.min.time())
    data = {"name": body["name"], "surname": body["surname"]}
    attendance = get_minor_attendances(db, att_date)
    if attendance:
        _id = ObjectId()
        data["minorId"] = id
        data["_id"] = _id
        data["date"] = att_date
        data["creation_date"] = att_date
        data["isPresent"] = False
        if "creation_user" in data:
            data["creation_user"] = ObjectId(data["creation_user"]["$oid"])
        db["minorAttendance"].update_one({"_id": _id}, {"$set": data}, upsert=True)
