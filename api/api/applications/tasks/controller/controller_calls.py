from datetime import datetime, timedelta

from bson import ObjectId

from api.applications.auth.helper.user import get_user
from api.applications.minors.helper.minor import get_minor
from api.applications.tasks.helper.call_logs import update_call_log
from api.applications.tasks.helper.medication import queryParams
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo
from api.utils.session import get_current_user


def tasks_call_logs(minor, operator, date, page=0, limit=8):
    date = datetime.combine(datetime.strptime(date, "%d/%m/%Y"), datetime.min.time()) if len(date) > 0 else date
    data = {
        "minors": ObjectId(minor) if len(minor) > 0 else minor,
        "creation_user": ObjectId(operator) if len(operator) > 0 else operator,
    }
    query = queryParams(data)
    if isinstance(date, datetime):
        query["date"] = {"$gte": date, "$lte": (date + timedelta(days=1))}
    db = get_mongo().cx.get_default_database()
    pipeline = [
        {"$match": {"$and": [query]}},
        {"$sort": {"date": -1}},  # Ordinamento inverso per il campo "date"
    ]
    pipeline += [
        {
            "$facet": {
                "paginatedResults": [{"$skip": page * limit}, {"$limit": limit}],
                "meta": [{"$count": "rowsNumber"}],
            }
        }
    ]
    pipeline += [{"$unwind": "$meta"}]
    pipeline += [{"$addFields": {"meta.page": (page + 1), "meta.rowsPerPage": limit}}]
    call_logs = list(db["callLogs"].aggregate(pipeline))
    if call_logs:
        call_logs = call_logs[0]
        for call in call_logs["paginatedResults"]:
            operator = get_user(db, call["creation_user"])
            if operator:
                call["operator"] = operator
            else:
                call["operator"] = None
            call["date"] = call["date"].strftime("%Y-%m-%d %H:%M:%S")
            minors = []
            for minor in call["minors"]:
                minors.append(get_minor(db, ObjectId(minor)))
            call["minors"] = minors
    return jsonify_mongo(call_logs)


def tasks_call_logs_post(body):
    db = get_mongo().cx.get_default_database()
    now = datetime.now()
    id = ObjectId()
    body["_id"] = id
    body["creation_date"] = now
    body["last_modified"] = now
    body["creation_user"] = ObjectId(get_current_user().uid)
    body["date"] = datetime.strptime(body["date"], "%d/%m/%Y %H:%M:%S")
    minors = []
    for minor in body["minors"]:
        minors.append(ObjectId(minor))
    body["minors"] = minors
    db["callLogs"].update_one({"_id": id}, {"$set": body}, upsert=True)
    return {"success": True}


def tasks_call_logs_arg_delete(arg):
    db = get_mongo().cx.get_default_database()
    db["callLogs"].delete_one({"_id": ObjectId(arg)})
    return {"success": True}


def tasks_call_logs_arg_put(arg, body):
    db = get_mongo().cx.get_default_database()
    minors = []
    for minor in body["minors"]:
        minors.append(ObjectId(minor))
    body["minors"] = minors
    if db["callLogs"].find_one({"_id": ObjectId(arg)}):
        return update_call_log(db, arg, body)
    else:
        return {"success": False, "msg": "Telefonata non trovata"}
