from datetime import datetime, timedelta

import pytz

from api.middleware.mongo import get_mongo
from api.utils.generic import get_dayofweek, get_shift


def get_next_shifts(shift, turni_in_avanti):
    shifts = ["Mattina", "Pomeriggio", "Sera"]
    index = shifts.index(shift)
    next_shifts = shifts[index:] + shifts[:index]
    return next_shifts[: turni_in_avanti + 1]


def update_task_status():
    db = get_mongo().cx.get_default_database()
    now = datetime.now(pytz.timezone("Europe/Rome"))
    get_dayofweek(now)
    current_day_plusone = get_dayofweek(now + timedelta(days=1))
    current_day_plustwo = get_dayofweek(now + timedelta(days=2))
    current_shift = get_shift(now)
    tasks_to_update = []

    if current_shift == "Mattina":
        tasks_to_update = db["notebookTasks"].find(
            {"dayofweek": current_day_plusone, "shifts": {"$in": ["Mattina", "Pomeriggio", "Sera"]}}
        )
    if current_shift == "Pomeriggio":
        tasks_to_update1 = db["notebookTasks"].find(
            {"dayofweek": current_day_plusone, "shifts": {"$in": ["Pomeriggio", "Sera"]}}
        )
        tasks_to_update2 = db["notebookTasks"].find({"dayofweek": current_day_plustwo, "shifts": {"$in": ["Mattina"]}})
        tasks_to_update = []
        tasks_to_update.extend(tasks_to_update1)
        tasks_to_update.extend(tasks_to_update2)
    if current_shift == "Sera":
        tasks_to_update1 = db["notebookTasks"].find({"dayofweek": current_day_plusone, "shifts": {"$in": ["Sera"]}})
        tasks_to_update2 = db["notebookTasks"].find(
            {"dayofweek": current_day_plustwo, "shifts": {"$in": ["Mattina", "Pomeriggio"]}}
        )
        tasks_to_update = []
        tasks_to_update.extend(tasks_to_update1)
        tasks_to_update.extend(tasks_to_update2)

    for task in tasks_to_update:
        db["notebookTasks"].update_one({"_id": task["_id"]}, {"$set": {"status": "active"}, "$unset": {"operator": 1}})
