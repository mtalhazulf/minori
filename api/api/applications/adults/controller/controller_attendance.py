from datetime import datetime

from bson import ObjectId
from flask import jsonify

from api.applications.adults.helper.adult import get_adult
from api.applications.adults.helper.attendance import add_adult_attendance
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo


def adults_attendance_arg_get(current_date):
    db = get_mongo().cx.get_default_database()
    current_date = datetime.strptime(current_date, "%Y/%m/%d")
    today = datetime.combine(current_date.date(), datetime.min.time())
    attendances = list(db["adultAttendance"].find({"date": today}))
    for attendance in attendances:
        if "adultId" in attendance:
            adult = get_adult(db, attendance["adultId"])
            if adult:
                attendance["name"] = adult["name"] if "name" in adult else attendance["name"]
                attendance["surname"] = adult["surname"] if "surname" in adult else attendance["surname"]
                attendance["fiscal_code"] = adult["fiscal_code"] if "fiscal_code" in adult else ""
    return jsonify_mongo(attendances)


def adults_attendance_post(body):
    for i in body:
        add_adult_attendance(i)
    return jsonify({"success": True})


def adults_attendance_month_arg_get(arg, start_date, end_date):
    db = get_mongo().cx.get_default_database()
    start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    attendances = list(
        db["adultAttendance"].find(
            {
                "date": {"$gte": start, "$lte": end},
                "isPresent": True,
                "adultId": ObjectId(arg),
            }
        )
    )
    return jsonify_mongo(attendances)
