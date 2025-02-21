from api.middleware.mongo import get_mongo


def get_user(code):
    # db = get_mongo().cx.get_default_database()
    db = get_mongo().cx.get_default_database()
    user = db["users"].find_one(
        {
            "badgeId": code,
            "$or": [{"status": "enabled"}, {"status": {"$exists": False}}],
        },
        {},
    )
    return user


def parseBadgeString(msg):
    chuncks = [2, 1, 1, 9, 4, 2, 2, 2, 2, 2, 2, 2]
    elements = [
        "Sense",
        "Type",
        "WDay",
        "NBadge",
        "ReasonCode",
        "H",
        "m",
        "Sec",
        "Day",
        "M",
        "Y",
        "Id",
    ]
    result = {}

    for i, chunk in enumerate(chuncks):
        result[elements[i]] = msg[0:chunk]
        msg = msg[chunk:]

    return result


def get_user_status(code):
    # db = get_mongo().cx.get_default_database()
    db = get_mongo().cx.get_default_database()
    user = get_user(code)
    if user:
        attendance = db["attendance"].find_one({"userId": user["_id"], "end_date": None})
        return {"status": -2} if attendance else {"status": 0}
    else:
        return {"status": -1}


def get_attendance_status(code):
    # db = get_mongo().cx.get_default_database()
    db = get_mongo().cx.get_default_database()
    user = get_user(code)
    if user:
        attendance = db["attendance"].find_one({"userId": user["_id"], "end_date": None})
        return {"status": 0} if attendance else {"status": -1}
    else:
        return {"status": -2}
