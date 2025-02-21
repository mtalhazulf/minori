from datetime import datetime

from bson import ObjectId
from flask import jsonify

from api.applications.minors.helper.attendance import add_minor_attendance
from api.applications.minors.helper.minor import get_minor
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo


def minors_attendance_arg_get(current_date):
    db = get_mongo().cx.get_default_database()
    current_date = datetime.strptime(current_date, "%Y/%m/%d")
    today = datetime.combine(current_date.date(), datetime.min.time())
    attendances = list(db["minorAttendance"].find({"date": today}))
    for attendance in attendances:
        if "minorId" in attendance:
            minor = get_minor(db, attendance["minorId"])
            if minor:
                attendance["name"] = minor["name"] if "name" in minor else attendance["name"]
                attendance["surname"] = minor["surname"] if "surname" in minor else attendance["surname"]
                attendance["fiscal_code"] = minor["fiscal_code"] if "fiscal_code" in minor else ""
    return jsonify_mongo(attendances)


def minors_attendance_post(body):
    for i in body:
        add_minor_attendance(i)
    return jsonify({"success": True})


def minors_attendance_month_arg_get(arg, start_date, end_date):
    db = get_mongo().cx.get_default_database()
    start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    attendances = list(
        db["minorAttendance"].find(
            {
                "date": {"$gte": start, "$lte": end},
                "isPresent": True,
                "minorId": ObjectId(arg),
            }
        )
    )
    return jsonify_mongo(attendances)
