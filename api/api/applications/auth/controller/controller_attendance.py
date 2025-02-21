from datetime import datetime

from bson import ObjectId
from flask import jsonify

from api.applications.auth.helper.attendance import (
    add_new_attendance,
    check_active_attendance,
    is_overlapping_attendances,
    is_overlapping_attendances2,
    is_overlapping_attendances3,
)
from api.applications.auth.helper.user import get_active_users, get_user
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo
from api.utils.session import get_current_user


def auth_attendance_active_get():
    db = get_mongo().cx.get_default_database()
    active_op = list(db["attendance"].find({"end_date": None, "status": "enabled"}, {"_id": 0, "userId": 1}))
    users = []
    for op in active_op:
        user = db["users"].find_one({"_id": op["userId"]})
        if "type" in user and user["type"] != "admin" and user["type"] != "superadmin":
            users.append(op["userId"])
    return jsonify_mongo(get_active_users(db, users))


def auth_attendance_status_get():
    db = get_mongo().cx.get_default_database()
    active_op = list(
        db["attendance"].find(
            {
                "$query": {
                    "$or": [
                        {"end_date": None},
                        {"end_date": {"$ne": None}, "status": "refused"},
                    ]
                },
                "$orderby": {"start_date": -1},
            }
        )
    )
    users = []
    for op in active_op:
        user = db["users"].find_one({"_id": op["userId"]})
        if "type" in user and user["type"] != "admin" and user["type"] != "superadmin":
            if "status" in op:
                user["status"] = op["status"]
            users.append(user)
    return jsonify_mongo(users)


def auth_attendance_arg_get(arg):
    db = get_mongo().cx.get_default_database()
    id = ObjectId(arg)
    return jsonify_mongo(list(db["attendance"].find({"_id": id})))


def auth_attendance_get():
    db = get_mongo().cx.get_default_database()
    attendances = list(
        db["attendance"].find(
            {
                "$query": {},
                "$orderby": {"start_date": -1},
            }
        )
    )
    for att in attendances:
        user = get_user(db, att["userId"])
        att["userId"] = user if user else "User"
        att["start_date"] = att["start_date"].strftime("%Y-%m-%d %H:%M")
        att["end_date"] = att["end_date"].strftime("%Y-%m-%d %H:%M") if att["end_date"] else None
    return jsonify_mongo(attendances)


def auth_attendance_put(body):
    db = get_mongo().cx.get_default_database()
    data_set = {"status": body["status"]}
    if body["status"] == "enabled":
        data_set["type"] = "blue"
    if body["status"] == "refused":
        data_set["end_date"] = datetime.now()
    if "start_date" in body:
        data_set["start_date"] = datetime.strptime(body["start_date"], "%d/%m/%Y %H:%M")
    else:
        data_set["start_date"] = datetime.now()
    db["attendance"].update_one(
        {
            "userId": ObjectId(body["user"]),
            "status": "pending",
            "end_date": None,
            "type": "red",
        },
        {"$set": data_set},
    )
    return jsonify({"success": True})


def auth_attendance_post(body):
    db = get_mongo().cx.get_default_database()

    if "end_date" not in body and check_active_attendance(db, body["userId"]):
        return jsonify(
            {
                "success": False,
                "msg": "L'operatore ha già effettuato la timbratura d'ingresso (e non " "d'uscita)",
            }
        )
    if "start_date" in body and "end_date" in body:
        start_date = datetime.strptime(body["start_date"], "%d/%m/%Y %H:%M")
        end_date = datetime.strptime(body["end_date"], "%d/%m/%Y %H:%M")
        if start_date > end_date:
            return {
                "success": False,
                "msg": "Ora inizio turno non può essere successiva ora fine turno",
            }
        if not is_overlapping_attendances2(db, body["userId"], body["start_date"], body["end_date"]):
            updated = add_new_attendance(db, body["userId"], get_current_user().usertype, body)
            if updated:
                return {"success": updated}
            else:
                return {
                    "success": updated,
                    "msg": "Errore durante l'inserimento della timbratura",
                }
    if (
        "start_date" in body
        and "end_date" not in body
        and not is_overlapping_attendances3(db, body["userId"], body["start_date"])
    ):
        updated = add_new_attendance(db, body["userId"], get_current_user().usertype, body)
        if updated:
            return {"success": updated}
        else:
            return {
                "success": updated,
                "msg": "Errore durante l'inserimento della timbratura",
            }
    return jsonify(
        {
            "success": False,
            "msg": "L'operatore ha già effettuato una timbratura per lo stesso orario",
        }
    )


def auth_attendance_out_arg_put(arg, body):
    db = get_mongo().cx.get_default_database()
    body["end_date"] = datetime.strptime(body["end_date"], "%d/%m/%Y %H:%M")
    attendance = db["attendance"].find_one({"_id": ObjectId(arg)})
    if attendance:
        user_id = attendance["userId"]
        notebookTasks = list(db["notebookTasks"].find({"operator": user_id, "status": "charged"}, {"_id": 1}))
        if len(notebookTasks) > 0:
            return jsonify({"success": False, "msg": "Mansione ancora da svolgere"})
        tasks = list(db["tasks"].find({"operator": user_id, "status": "charged"}, {"_id": 1}))
        if len(tasks) > 0:
            return jsonify({"success": False, "msg": "Consegna ancora da svolgere"})
    else:
        return jsonify(
            {
                "success": False,
                "msg": "L'uscita non è stata inserita correttamente.",
            }
        )
    if not is_overlapping_attendances(db, arg, body["end_date"]):
        updated = db["attendance"].update_one(
            {
                "_id": ObjectId(arg),
            },
            {"$set": body},
        )
        if updated.matched_count > 0:
            return jsonify({"success": True})
        else:
            return jsonify(
                {
                    "success": False,
                    "msg": "L'uscita non è stata inserita correttamente.",
                }
            )
    else:
        return jsonify({"success": False, "msg": "Non è possibile sovrapporre due timbrature"})


def auth_attendance_operator_arg_get(arg, start_date, end_date):
    db = get_mongo().cx.get_default_database()
    start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    attendances = list(
        db["attendance"].find(
            {
                "$query": {
                    "userId": ObjectId(arg),
                    "status": {"$ne": "refused"},
                    "end_date": {"$ne": None},
                    "start_date": {"$gte": start, "$lte": end},
                },
                "$orderby": {"start_date": -1},
            }
        )
    )
    for att in attendances:
        att["start_date"] = att["start_date"].strftime("%Y-%m-%d %H:%M")
        att["end_date"] = att["end_date"].strftime("%Y-%m-%d %H:%M") if att["end_date"] else None
    return jsonify_mongo(attendances)
