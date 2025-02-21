from datetime import date, datetime, timedelta

from bson import ObjectId
from flask import jsonify, request

from api.applications.tasks.helper.logbook import update_logbook
from api.applications.tasks.helper.notebook import (
    get_notebook_tasks,
    get_summary,
    get_taken_tasks,
)
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo
from api.utils.db_task_reset import update_task_status
from api.utils.session import get_current_user


def tasks_notebook_reset_get():
    update_task_status()
    return {"success": True}


def tasks_notebook_taken_get(days_or_date):
    db = get_mongo().cx.get_default_database()
    args = request.args.to_dict()
    return jsonify_mongo(get_taken_tasks(db, None, days_or_date, args, None))


def tasks_notebook_arg_get(shift, dayofweek, data):
    db = get_mongo().cx.get_default_database()
    return jsonify_mongo(get_notebook_tasks(db, shift, dayofweek, data))


def tasks_notebook_arg_post(shift, dayofweek, data, body):
    db = get_mongo().cx.get_default_database()
    operator = ObjectId(get_current_user().uid)
    today = datetime.combine(date.today(), datetime.min.time())
    tomorrow = today + timedelta(1)
    for id in body["charge"]:
        taskLog = db["notebookLog"].find_one(
            {"task": ObjectId(id), "date": {"$gte": today, "$lte": tomorrow}, "shifts": shift, "dayofweek": dayofweek}
        )
        task = db["notebookTasks"].find_one({"_id": ObjectId(id)})
        if task:
            db["notebookTasks"].update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                        "status": "charged",
                        "operator": operator,
                    }
                },
                upsert=True,
            )
        if not taskLog:
            _id = ObjectId()
            db["notebookLog"].update_one(
                {"_id": ObjectId(_id)},
                {
                    "$set": {
                        "task": ObjectId(id),
                        "operator": operator,
                        "date": datetime.now(),
                        "shifts": shift,
                        "dayofweek": dayofweek,
                        "status": "charged",
                    }
                },
                upsert=True,
            )
    for id in body["discharge"]:
        taskLog = db["notebookLog"].find_one(
            {"task": ObjectId(id), "date": {"$gte": today, "$lte": tomorrow}, "shifts": shift, "dayofweek": dayofweek}
        )
        task = db["notebookTasks"].find_one({"_id": ObjectId(id)})
        if task:
            db["notebookTasks"].update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                        "status": "active",
                    }
                },
                upsert=True,
            )
            if "operator" in task:
                db["notebookTasks"].update_one(
                    {"_id": ObjectId(id)},
                    {"$unset": {"operator": 1}},
                )
        if taskLog:
            _id = taskLog["_id"]
            db["notebookLog"].delete_one({"_id": ObjectId(_id)})
    return {"success": True}


def tasks_notebook_post(body):
    db = get_mongo().cx.get_default_database()
    today = datetime.now()
    for period in body["periods"]:
        existing_record = db["notebookTasks"].find_one(
            {"title": body["title"], "shifts": [period["shift"]], "dayofweek": [period["dayofweek"]]}
        )
        if existing_record:
            return {"error: trying to insert same task in the same period": False}, 409

        db["notebookTasks"].insert_one(
            {
                "title": body["title"],
                "description": body["description"],
                "dayofweek": [period["dayofweek"]],
                "shifts": [period["shift"]],
                "status": "active",
                "creation_date": today,
            }
        )
    return {"success": True}


def tasks_notebook_put(body):
    db = get_mongo().cx.get_default_database()
    notebookTask = db["notebookTasks"].find_one({"_id": ObjectId(body["task"])})
    if notebookTask:
        if body["isAccepted"]:
            # update_logbook(db, ObjectId(body["task"]), "notebook_tasks", body["date"], shift, "Mansione svolta")
            db["notebookLog"].update_one(
                {
                    "task": ObjectId(body["task"]),
                    "status": "charged",
                },
                {"$set": {"status": "done"}},
            )
            db["notebookTasks"].update_one(
                {"_id": ObjectId(body["task"])},
                {
                    "$set": {
                        "status": "done",
                    }
                },
                upsert=False,
            )
        else:
            db["notebookLog"].delete_one({"task": ObjectId(body["task"])})
            # update_logbook(db, ObjectId(body["task"]), "notebook_tasks", body["date"], shift, "Mansione non svolta")
            db["notebookTasks"].update_one(
                {"_id": ObjectId(body["task"])},
                {
                    "$set": {
                        "status": "active",
                    },
                    "$unset": {"operator": 1},
                },
                upsert=False,
            )
        return {"success": True}
    else:
        return jsonify({"success": False, "message": "notebookTask not found."}), 404


def tasks_notebook_notes_put(body):
    db = get_mongo().cx.get_default_database()
    if body["notes"]:
        update_logbook(db, ObjectId(body["task"]), "notebook_tasks", body["date"], body["shift"], body["notes"])


def tasks_notebook_summary_arg_get(shift, dayofweek):
    db = get_mongo().cx.get_default_database()
    return get_summary(db, shift, dayofweek)


def tasks_notebook_type_arg_get(arg):
    db = get_mongo().cx.get_default_database()
    tasks = list(
        db["notebookTasks"].find(
            {"$or": [{"status": "active"}, {"status": "charged"}, {"status": "done"}], "title": arg}
        )
    )
    return tasks


def tasks_notebook_arg_delete(arg, shift, dayofweek):
    db = get_mongo().cx.get_default_database()
    task = db["notebookTasks"].find_one({"_id": ObjectId(arg)})
    if task and task["dayofweek"] == [dayofweek] and task["shifts"] == [shift]:
        result = db["notebookTasks"].delete_one({"_id": ObjectId(arg)})
        if result.deleted_count > 0:
            result = db["notebookLog"].delete_many({"task": ObjectId(arg)})
            if result.deleted_count > 0:
                return {"success": True}
            else:
                return {"error: unable to delete notebookLog related at notebook": False}, 404
        else:
            return {"error: unable to delete notebook": False}, 404
    else:
        return {"error: data in DB do not match with info provided": False}, 404
