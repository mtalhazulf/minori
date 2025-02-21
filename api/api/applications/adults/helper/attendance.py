from datetime import date, datetime

from bson import ObjectId

from api.middleware.mongo import get_mongo


def get_adult_attendance(db, id, date):
    attendance = list(db["adultAttendance"].find({"_id": id, "date": date}))
    return True if len(attendance) > 0 else False


def get_adult_attendances(db, date):
    attendance = list(db["adultAttendance"].find({"date": date}))
    return True if len(attendance) > 0 else False


def add_adult_attendance(data):
    db = get_mongo().cx.get_default_database()
    att_date = datetime.combine(date.today(), datetime.min.time())
    if get_adult_attendance(db, ObjectId(data["_id"]["$oid"]), att_date):
        db["adultAttendance"].update_one(
            {"_id": ObjectId(data["_id"]["$oid"])},
            {"$set": {"isPresent": data["isPresent"]}},
        )
    else:
        id = ObjectId()
        data["adultId"] = ObjectId(data["_id"]["$oid"])
        data["_id"] = id
        data["date"] = att_date
        data["creation_date"] = att_date
        if "creation_user" in data:
            data["creation_user"] = ObjectId(data["creation_user"]["$oid"])
        db["adultAttendance"].update_one({"_id": id}, {"$set": data}, upsert=True)


def update_attendances(db, id):
    adult = db["adults"].find_one({"_id": ObjectId(id)})
    if adult:
        db["adultAttendance"].update(
            {
                "adultId": ObjectId(id),
            },
            {"$set": {"name": adult["name"], "surname": adult["surname"]}},
        )


def check_attendance(db, id, body):
    att_date = datetime.combine(date.today(), datetime.min.time())
    data = {"name": body["name"], "surname": body["surname"]}
    attendance = get_adult_attendances(db, att_date)
    if attendance:
        _id = ObjectId()
        data["adultId"] = id
        data["_id"] = _id
        data["date"] = att_date
        data["creation_date"] = att_date
        data["isPresent"] = False
        if "creation_user" in data:
            data["creation_user"] = ObjectId(data["creation_user"]["$oid"])
        db["adultAttendance"].update_one({"_id": _id}, {"$set": data}, upsert=True)
