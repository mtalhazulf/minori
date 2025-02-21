from datetime import date, datetime, timedelta

from bson import ObjectId

from api.applications.adults.helper.adult import get_adult
from api.applications.auth.helper.user import get_user
from api.applications.minors.helper.minor import get_minor
from api.applications.settings.helper.settings import get_resource
from api.utils.generic import get_dayofweek, get_shift


def get_taken_tasks(db, days_or_date, args=None, state=None):
    today = datetime.combine(date.today(), datetime.min.time())
    end = today + timedelta(1)
    try:
        start = today - timedelta(int(days_or_date))
    except ValueError:
        start = datetime.strptime(days_or_date, "%Y-%m-%d")
        end = start + timedelta(1)
    query = {"start": {"$gte": start, "$lte": end}, "selected": True}
    if args:
        query["operator"] = ObjectId(args["user"])
    if state:
        query["status"] = state
    tasks = list(db["tasks"].find(query))
    for task in tasks:
        task["shift"] = get_shift(task["start"])
        task["start"] = task["start"].strftime("%Y-%m-%d %H:%M:%S")
        task["dayofweek"] = get_dayofweek(task["start"])
        operator = get_user(db, task["operator"])
        if operator:
            task["operator"] = operator
        else:
            task["operator"] = "Admin"
    return tasks


def get_events(db, data):
    data["startdate"] = datetime.strptime(data["startdate"], "%Y-%m-%dT%H:%M:%S.%fZ")
    data["enddate"] = datetime.strptime(data["enddate"], "%Y-%m-%dT%H:%M:%S.%fZ")
    start_date = datetime.combine(data["startdate"].date(), datetime.min.time())
    end_date = datetime.combine(data["enddate"].date(), datetime.min.time())
    events = list(db["tasks"].find({"start": {"$gte": start_date, "$lte": end_date}}))
    for event in events:
        event["start"] = event["start"].strftime("%Y-%m-%d %H:%M:%S")
        if "minor" in event:
            minor = get_minor(db, event["minor"])
            event["minor"] = minor if minor else "Minore"
        if "adult" in event:
            adult = get_adult(db, event["adult"])
            event["adult"] = adult if adult else "Adulto"
        if "resource" in event:
            resource_module, resource_type = get_resource(db, event["resource"]["module"], event["resource"]["type"])
            event["resource"]["module"] = resource_module if resource_module else "Modulo HCCP"
            event["resource"]["type"] = resource_type if resource_type else ""
        if "operator" in event:
            operator = get_user(db, event["operator"])
            event["operator"] = operator if operator else "User"

    return events


def get_tasks(db, data):
    data["today_date"] = datetime.strptime(data["today_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    today = datetime.combine(data["today_date"].date(), datetime.min.time())
    tomorrow = today + timedelta(1)
    tasks = list(db["tasks"].find({"start": {"$gte": today, "$lte": tomorrow}}))
    for task in tasks:
        task["start"] = task["start"].strftime("%Y-%m-%d %H:%M:%S")
        if "minor" in task:
            minor = get_minor(db, task["minor"])
            task["minor"] = minor if minor else "Minore"
        if "adult" in task:
            adult = get_adult(db, task["adult"])
            task["adult"] = adult if adult else "Adulto"
        if "resource" in task:
            resource_module, resource_type = get_resource(db, task["resource"]["module"], task["resource"]["type"])
            task["resource"]["module"] = resource_module if resource_module else "Modulo HCCP"
            task["resource"]["type"] = resource_type if resource_type else ""
        if "operator" in task:
            operator = get_user(db, task["operator"])
            task["operator"] = operator if operator else "User"
    return tasks
