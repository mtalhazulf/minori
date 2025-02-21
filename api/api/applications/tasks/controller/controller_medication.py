from datetime import datetime

from bson import ObjectId

from api.applications.auth.helper.user import get_user
from api.applications.tasks.helper.medication import queryParams, update_medication
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo
from api.utils.session import get_current_user


def tasks_medication_get(name, amount, operator, expiration_date, disposed_of, page=0, limit=8):
    expiration_date = (
        datetime.combine(datetime.strptime(expiration_date, "%d/%m/%Y"), datetime.min.time())
        if len(expiration_date) > 0
        else expiration_date
    )
    data = {
        "name": name,
        "amount": amount,
        "creation_user": ObjectId(operator) if len(operator) > 0 else operator,
        "expiration_date": expiration_date,
    }
    if disposed_of != "":
        data["disposed_of"] = disposed_of == "true"
    query = [queryParams(data)]
    pipeline = [{"$match": {"$and": query}}, {"$sort": {"expiration_date": 1}}]
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
    db = get_mongo().cx.get_default_database()
    medication = list(db["medication"].aggregate(pipeline))
    if medication:
        medication = medication[0]
        for med in medication["paginatedResults"]:
            creation_user = get_user(db, med["creation_user"])
            if creation_user:
                med["creation_user"] = creation_user
            else:
                med["creation_user"] = "Admin"
            med["expiration_date"] = med["expiration_date"].strftime("%Y-%m-%d %H:%M:%S")
    return jsonify_mongo(medication)


def tasks_medication_post(body):
    db = get_mongo().cx.get_default_database()
    now = datetime.now()
    id = ObjectId()
    body["_id"] = id
    body["creation_date"] = now
    body["last_modified"] = now
    body["creation_user"] = ObjectId(get_current_user().uid)
    body["expiration_date"] = datetime.combine(
        datetime.strptime(body["expiration_date"], "%d/%m/%Y"), datetime.min.time()
    )
    db["medication"].update_one({"_id": id}, {"$set": body}, upsert=True)
    return {"success": True}


def tasks_medication_arg_delete(arg):
    db = get_mongo().cx.get_default_database()
    db["medication"].delete_one({"_id": ObjectId(arg)})
    return {"success": True}


def tasks_medication_arg_put(arg, body):
    db = get_mongo().cx.get_default_database()
    if db["medication"].find_one({"_id": ObjectId(arg)}):
        return update_medication(db, arg, body)
    else:
        return {"success": False, "msg": "Farmaco non trovato"}
