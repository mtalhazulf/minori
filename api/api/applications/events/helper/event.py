from datetime import datetime, timedelta

from api.applications.auth.helper.user import get_user
from api.applications.minors.helper.minor import get_minor


def get_events(db, data):
    data["date"] = datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(day=1)
    start_date = datetime.combine(data["date"].date(), datetime.min.time())
    end_date = start_date.replace(month=1 if start_date.month == 12 else start_date.month + 1)
    events = list(db["events"].find({"start": {"$gte": start_date, "$lte": end_date}}))
    for event in events:
        event["start"] = event["start"].strftime("%Y-%m-%d %H:%M:%S")
        if "minor" in event:
            minor = get_minor(db, event["minor"])
            event["minor"] = minor if minor else "Minore"
        if "operator" in event:
            operator = get_user(db, event["operator"])
            event["operator"] = operator if operator else "User"

    return events


def get_tasks(db, data):
    data["today_date"] = datetime.strptime(data["today_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    today = datetime.combine(data["today_date"].date(), datetime.min.time())
    tomorrow = today + timedelta(1)
    tasks = list(db["events"].find({"start": {"$gte": today, "$lte": tomorrow}}))
    for task in tasks:
        task["start"] = task["start"].strftime("%Y-%m-%d %H:%M:%S")
        if "minor" in task:
            minor = get_minor(db, task["minor"])
            task["minor"] = minor if minor else "Minore"
        if "operator" in task:
            operator = get_user(db, task["operator"])
            task["operator"] = operator if operator else "User"
    return tasks
