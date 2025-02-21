from datetime import date, datetime, timedelta

from bson import ObjectId

from api.applications.auth.helper.user import get_user
from api.applications.minors.helper.minor import get_minor
from api.utils.session import get_current_user


def get_taken_tasks(db, shift, days_or_date, args=None, state=None):
    today = datetime.combine(date.today(), datetime.min.time())
    end = today + timedelta(1)
    try:
        start = today - timedelta(int(days_or_date))
    except ValueError:
        start = datetime.strptime(days_or_date, "%Y-%m-%d")
        end = start + timedelta(1)
    if shift:
        query = {"date": {"$gte": start, "$lte": end}, "shifts": shift}
    else:
        query = {"date": {"$gte": start, "$lte": end}}
    if args:
        query["operator"] = ObjectId(args["user"])
    if state:
        query["status"] = state
    tasks = list(db["notebookLog"].find(query))
    for task in tasks:
        task["date"] = task["date"].strftime("%Y-%m-%d %H:%M:%S")
        if taskFromDB := db["notebookTasks"].find_one({"_id": task["task"]}):
            task["task"] = taskFromDB
        # else:
        #     db["notebookLog"].delete_many({"task": task["task"]}) # elementi rimasti orfani che si possono rimuovere
        operator = get_user(db, task["operator"])
        if operator:
            task["operator"] = operator
        else:
            task["operator"] = "Admin"
    return tasks


def get_notebook_tasks(db, shift, dayofweek, data):
    date = datetime.strptime(data, "%Y-%m-%d")
    tasks = list(
        db["notebookTasks"].find(
            {
                "$or": [{"status": "active"}, {"status": "charged"}, {"status": "done"}],
                "shifts": shift,
                "dayofweek": dayofweek,
            }
        )
    )
    for task in tasks:
        logs = get_task_log(db, task["_id"])
        if logs.count() == 0:
            task["selected"] = False
        for log in logs:
            if log["date"].date() == date.date():
                task["selected"] = True if log["status"] in ["charged", "done"] else False
                operator = get_user(db, log["operator"])
                if operator:
                    task["operator"] = operator
                else:
                    task["operator"] = "User"
            else:
                task["selected"] = False
        if "minors" in task:
            minors = []
            for minor in task["minors"]:
                min = get_minor(db, ObjectId(minor))
                minors.append(min if min else "minore")
            task["minors"] = minors
    return tasks


def get_task_log(db, id):
    return db["notebookLog"].find({"task": id})


def get_summary(db, shift, dayofweek):
    total = len(get_notebook_tasks(db, shift, dayofweek, str(datetime.now().date())))
    taken = (
        len(get_taken_tasks(db, shift, 0, {"user": ObjectId(get_current_user().uid)}))
        if get_current_user().usertype == "user"
        else len(get_taken_tasks(db, shift, 0))
    )
    done = len(get_taken_tasks(db, shift, 0, None, "done"))
    return {"total": total, "taken": taken, "done": done}
