from datetime import datetime

from bson import ObjectId
from flask import jsonify, request

from api.applications.tasks.helper.logbook import update_logbook
from api.applications.tasks.helper.task import get_events, get_taken_tasks, get_tasks
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo
from api.utils.generic import get_shift
from api.utils.session import get_current_user


def tasks_task_taken_get(days_or_date):
    db = get_mongo().cx.get_default_database()
    args = request.args.to_dict()
    args = None if "user" not in args else args
    return jsonify_mongo(get_taken_tasks(db, days_or_date, args))


def tasks_task_get():
    db = get_mongo().cx.get_default_database()
    if request.args and "startdate" in request.args.to_dict():
        return jsonify_mongo(get_events(db, request.args.to_dict()))
    if request.args and "today_date" in request.args.to_dict():
        return jsonify_mongo(get_tasks(db, request.args.to_dict()))


def tasks_task_charge_post(body):
    db = get_mongo().cx.get_default_database()
    operator = ObjectId(get_current_user().uid)
    if "charge" in body:
        for id in body["charge"]:
            task = db["tasks"].find_one({"_id": ObjectId(id), "selected": True})
            if not task:
                db["tasks"].update_one(
                    {"_id": ObjectId(id)},
                    {
                        "$set": {
                            "selected": True,
                            "operator": operator,
                            "status": "charged",
                        },
                        "$push": {
                            "log": {
                                "status": "charged",
                                "date": datetime.now(),
                                "operator": operator,
                            }
                        },
                    },
                )
    if "discharge" in body:
        for id in body["discharge"]:
            task = db["tasks"].find_one({"_id": ObjectId(id), "selected": False})
            if not task:
                db["tasks"].update_one(
                    {"_id": ObjectId(id)},
                    {
                        "$set": {"selected": False, "status": "open"},
                        "$push": {
                            "log": {
                                "status": "discharged",
                                "date": datetime.now(),
                                "operator": operator,
                            }
                        },
                        "$unset": {"operator": ""},
                    },
                )
    return {"success": True}


def tasks_task_post(body):
    db = get_mongo().cx.get_default_database()
    _id = ObjectId()
    today = datetime.now()
    if "minor" in body and body["minor"] is not None:
        body["minor"] = ObjectId(body["minor"])
        del body["resource"]
    if "adult" in body and body["adult"] is not None:
        body["adult"] = ObjectId(body["adult"])
        del body["resource"]
    if "resource" in body and body["resource"]["module"] is not None:
        del body["minor"]
    body["start"] = datetime.strptime(body["start"], "%d/%m/%Y %H:%M")
    db["tasks"].update_one(
        {"_id": ObjectId(_id)},
        {"$set": {**body, "status": "open", "creation_date": today, "selected": False}},
        upsert=True,
    )
    return {"success": True}


def tasks_task_put(body):
    db = get_mongo().cx.get_default_database()
    task = db["tasks"].find_one({"_id": ObjectId(body["task"])})
    update = {}
    if task:
        # date = task["start"].strftime("%Y-%m-%d 00:00:00")
        get_shift(task["start"])
        if body["isAccepted"]:
            # update_logbook(db, ObjectId(body["task"]), "tasks", date, shift, "Consegna svolta")
            update = {
                "$set": {"status": "done"},
                "$push": {
                    "log": {
                        "status": "done",
                        "date": datetime.now(),
                        "operator": ObjectId(get_current_user().uid),
                    }
                },
            }

        else:
            subquery = {"selected": False, "status": "open"}
            if "postponed" in body:
                subquery["postponed"] = True
            if "note" in body:
                subquery["note"] = body["note"]
            update = {
                "$set": subquery,
                "$push": {
                    "log": {
                        "status": "discharged",
                        "date": datetime.now(),
                        "operator": ObjectId(get_current_user().uid),
                    }
                },
                "$unset": {"operator": ""},
            }
            # update_logbook(db, ObjectId(body["task"]), "tasks", date, shift, "Consegna non svolta")
        db["tasks"].update_one(
            {"_id": ObjectId(body["task"])},
            update,
        )
        return {"success": True}
    else:
        return jsonify({"success": False, "message": "Task not found."}), 404


def tasks_task_notes_put(body):
    db = get_mongo().cx.get_default_database()
    if body["notes"]:
        update_logbook(db, ObjectId(body["task"]), "tasks", body["date"], body["shift"], body["notes"])


def tasks_task_summary_get():
    db = get_mongo().cx.get_default_database()
    today_date = str(datetime.now().date()) + "T" + str(datetime.now().time()) + "Z"
    total = len(get_tasks(db, {"today_date": today_date}))
    taken = (
        len(get_taken_tasks(db, 0, {"user": ObjectId(get_current_user().uid)}, "charged"))
        if get_current_user().usertype == "user"
        else len(get_taken_tasks(db, 0, None, "charged"))
    )
    done = len(get_taken_tasks(db, 0, None, "done"))
    return {"total": total, "taken": taken, "done": done}


def tasks_task_arg_delete(arg):
    db = get_mongo().cx.get_default_database()
    db["tasks"].delete_one({"_id": ObjectId(arg)})
    return {"success": True}


def tasks_task_arg_put(body, arg):
    db = get_mongo().cx.get_default_database()
    task = db["tasks"].find_one({"_id": ObjectId(arg), "status": "open"})

    if task:
        if "start" in body:
            start = datetime.strptime(body["start"], "%d/%m/%Y %H:%M")
            body.pop("start")
        else:
            start = task["start"]
        if body["isGeneral"] == "True":
            if "adult" not in task and "minor" not in task:
                db["tasks"].update_one(
                    {"_id": ObjectId(arg)},
                    {
                        "$set": {
                            **body,
                            "start": start,
                        }
                    },
                )
            if "adult" in task:
                db["tasks"].update_one(
                    {"_id": ObjectId(arg)},
                    {
                        "$set": {
                            **body,
                            "start": start,
                        },
                        "$unset": {"adult": 1, "guest": 1},
                    },
                )
            if "minor" in task:
                db["tasks"].update_one(
                    {"_id": ObjectId(arg)},
                    {
                        "$set": {
                            **body,
                            "start": start,
                        },
                        "$unset": {"minor": 1, "guest": 1},
                    },
                )
        else:
            if "minor" in body and body["minor"] is not None:
                body["minor"] = ObjectId(body["minor"])
            if "adult" in body and body["adult"] is not None:
                body["adult"] = ObjectId(body["adult"])
            db["tasks"].update_one(
                {"_id": ObjectId(arg)},
                {
                    "$set": {
                        **body,
                        "start": start,
                    },
                },
            )
        return {"success": True}
    else:
        return {"error: unable to permorm the task": False}, 404
