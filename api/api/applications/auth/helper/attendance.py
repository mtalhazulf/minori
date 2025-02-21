from datetime import datetime, timedelta

from bson import ObjectId
from werkzeug.exceptions import BadRequest

from api.middleware.mongo import get_mongo


def are_intervals_overlapping(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1


def is_date_within(date, start, end):
    return start <= date <= end


def add_attendance(data, start_date):
    db = get_mongo().cx.get_default_database()
    if not check_attendance(db, data):
        updated = add_new_attendance(db, data.json["uid"], data.json["usertype"], start_date)
        if updated:
            return check_attendance(db, data)
        else:
            return False
    else:
        return True


def add_new_attendance(db, uid, usertype, data=None):
    now = datetime.now()
    id = ObjectId()
    attendance = {
        "_id": id,
        "userId": ObjectId(uid),
        "start_date": (
            datetime.strptime(data["start_date"], "%d/%m/%Y %H:%M")
            if data is not None and "start_date" in data
            else now
        ),
        "end_date": (
            datetime.strptime(data["end_date"], "%d/%m/%Y %H:%M") if data is not None and "end_date" in data else None
        ),
        "creation_date": now,
        "last_update": now,
        "type": data["type"] if data is not None and "type" in data else "red",
        "status": "pending" if (usertype != "admin" and usertype != "superadmin") else "enabled",
    }
    updated = db["attendance"].update_one({"_id": id}, {"$set": attendance}, upsert=True)
    if updated.upserted_id is not None:
        return True
    else:
        return False


def check_attendance(db, data):
    attendance = db["attendance"].find_one(
        {
            "userId": ObjectId(data.json["uid"]),
            "status": "pending",
            "end_date": None,
            "type": "red",
        }
    )
    if attendance:
        return True
    else:
        return False


def can_manual_login(sub, start_date, id):
    db = get_mongo().cx.get_default_database()
    start = datetime.strptime(start_date, "%d/%m/%Y %H:%M")
    attendance = db["attendance"].find_one({"userId": ObjectId(id), "end_date": None})
    if attendance:
        if attendance["status"] == "pending":
            return (
                False,
                "Impossibile accedere. L'amministratore non ha ancora accettato la richiesta di accesso!",
            )
        else:
            return (False, "Impossibile timbrare. Esiste già una timbratura in corso!")
    else:
        attendances_userId = list(db["attendance"].find({"userId": ObjectId(id)}))
        for attendance in attendances_userId:
            if is_date_within(start, attendance["start_date"], attendance["end_date"]):
                return (
                    False,
                    "Impossibile accedere. Ora attuale già presente in un precedente intervallo",
                )
    return (True, "")


def can_login(sub, id):
    db = get_mongo().cx.get_default_database()
    attendance = db["attendance"].find_one({"userId": ObjectId(id), "end_date": None})
    if attendance:
        return (
            (
                False,
                "Impossibile accedere. L'amministratore non ha ancora accettato la richiesta di accesso!",
            )
            if attendance["status"] == "pending"
            else (True, "L'operatore può loggarsi")
        )
    else:
        att = db["attendance"].find_one({"$query": {"userId": ObjectId(id)}, "$orderby": {"$natural": -1}})
        if att and att["end_date"] is not None and att["status"] == "refused":
            return (
                False,
                "Impossibile accedere. L'amministratore ha rifiutato l'ultima richiesta effettuata! "
                "Ripetere la timbratura e avvertire l'amministratore",
            )
        else:
            return (
                False,
                "Impossibile accedere. L'operatore non può accedere prima di aver timbrato!",
            )


def check_active_attendance(db, id):
    attendance = db["attendance"].find_one({"userId": ObjectId(id), "end_date": None})
    if attendance:
        return True
    else:
        return False


def is_overlapping_attendances3(db, id, date_str):
    date = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
    date += timedelta(minutes=1)

    attendances = list(
        db["attendance"].find({"userId": ObjectId(id), "start_date": {"$lte": date}, "end_date": {"$gte": date}})
    )
    return True if len(attendances) > 0 else False


def is_overlapping_attendances2(db, id, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%d/%m/%Y %H:%M")
    end_date = datetime.strptime(end_date_str, "%d/%m/%Y %H:%M")

    # Verifica sovrapposizione degli intervalli temporali
    query = {
        "userId": ObjectId(id),
        "$or": [
            {"start_date": {"$lt": end_date}, "end_date": {"$gt": start_date}},
            {"start_date": {"$lt": end_date}, "end_date": {"$gt": end_date}},
            {"start_date": {"$lt": start_date}, "end_date": {"$gt": start_date}},
        ],
    }

    attendances = list(db["attendance"].find(query))
    return True if len(attendances) > 0 else False


def is_overlapping_attendances(db, id, end_date):
    specific_record = db["attendance"].find_one({"_id": ObjectId(id)})

    if specific_record:
        start_date = specific_record["start_date"]
        userId = specific_record["userId"]

        # Controlla se c'è sovrapposizione con altri periodi nella collezione
        attendances_userId = list(db["attendance"].find({"userId": userId}))

        if specific_record in attendances_userId:
            attendances_userId.remove(specific_record)

        # Verifica se c'è sovrapposizione con l'intervallo del record specifico
        for attendance in attendances_userId:
            if are_intervals_overlapping(attendance["start_date"], attendance["end_date"], start_date, end_date):
                return True

        return False
    else:
        raise BadRequest()


# def get_attendance(db, user_id):
#     attendances = list(db["attendance"].find({"userId": ObjectId(user_id)}))
#     print("Attendances is ", attendances)
#     return attendances
def get_hours_worked(db, user_id):
    attendances = list(db["attendance"].find({"userId": ObjectId(user_id)}))
    total_hours = 0

    for attendance in attendances:
        start_date = attendance.get("start_date")
        end_date = attendance.get("end_date")

        if end_date is None or start_date is None:
            continue

        duration = end_date - start_date
        duration_hours = duration.total_seconds() / 3600  # Convert seconds to hours
        total_hours += duration_hours

    return total_hours
