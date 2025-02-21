from datetime import datetime

from bson import ObjectId

from api.applications.stamping.helper.stamp import (
    get_attendance_status,
    get_user,
    get_user_status,
    parseBadgeString,
)
from api.middleware.mongo import get_mongo


def stamping_stamp_in(body):  # /in/code
    user_status = get_user_status(body["id"])
    if user_status["status"] == 0:
        return stamping_stamp("in", body)
    else:
        return user_status


def stamping_stamp_out(body):  # /out/code
    user_status = get_attendance_status(body["id"])
    if user_status["status"] == 0:
        return stamping_stamp("out", body)
    else:
        return user_status


def stamping_stamp(_type, body):
    # db = get_mongo().cx.get_default_database()
    db = get_mongo().cx.get_default_database()
    parsed_string = parseBadgeString(body["attendance"])
    attendance_date = (
        parsed_string["Y"]
        + "-"
        + parsed_string["M"]
        + "-"
        + parsed_string["Day"]
        + " "
        + parsed_string["H"]
        + ":"
        + parsed_string["m"]
        + ":"
        + parsed_string["Sec"]
    )

    now = datetime.now()
    user_id = get_user(parsed_string["NBadge"])
    user_id = user_id["_id"]
    if parsed_string["Sense"] == "VE" and _type == "in" and get_user_status(parsed_string["NBadge"])["status"] == 0:
        id = ObjectId()
        attendance = {
            "_id": id,
            "start_date": datetime.strptime(attendance_date, "%y-%m-%d %H:%M:%S"),
            "userId": user_id,
            "end_date": None,
            "creation_date": now,
            "last_update": now,
            "type": "green",
            "status": "enabled",
            "macaddress": body["macaddress"] if "macaddress" in body else None,
        }
        db["attendance"].update_one({"_id": id}, {"$set": attendance}, upsert=True)

    elif (
        parsed_string["Sense"] == "VU"
        and _type == "out"
        and get_attendance_status(parsed_string["NBadge"])["status"] == 0
    ):
        notebookTasks = list(db["notebookTasks"].find({"operator": user_id, "status": "charged"}, {"_id": 1}))
        if len(notebookTasks) > 0:
            return {"status": 1}
        tasks = list(db["tasks"].find({"operator": user_id, "status": "charged"}, {"_id": 1}))
        if len(tasks) > 0:
            return {"status": 1}

        attendance = list(db["attendance"].find({"userId": user_id, "end_date": None}, {"_id": 1}))
        if len(attendance) > 0:
            id = attendance[0]["_id"]
            if id:
                attendance = {
                    "end_date": datetime.strptime(attendance_date, "%y-%m-%d %H:%M:%S"),
                    "last_update": now,
                }
                db["attendance"].update_one(
                    {"_id": id},
                    {
                        "$set": attendance,
                    },
                )
        else:
            return {"status": -1}
    else:
        return {"status": -1}

    return {"status": 0}
