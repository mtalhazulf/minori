from datetime import datetime

from bson import ObjectId

from api.utils.generic import get_dayofweek
from api.utils.session import get_current_user


def update_logbook(db, id, field, date, shift, notes):
    day_of_week = get_dayofweek(date)
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    operator = get_current_user().uid
    log = db["logbook"].find_one({"date": date, "shift": shift})
    if log:
        field_value = f"{field}"
        condition = {"_id": log["_id"], f"{field_value}.operator": ObjectId(operator)}

        if element := next((x for x in log.get(f"{field}", []) if x["operator"] == ObjectId(operator)), None):
            element["notes"] = notes
            update = {"$set": {f"{field}.$": element}}
            db["logbook"].update_one(condition, update)
        else:
            if id:
                new_element = {"id": ObjectId(id), "notes": notes, "operator": ObjectId(operator)}
            else:
                new_element = {"notes": notes, "operator": ObjectId(operator)}
            db["logbook"].update_one({"_id": log["_id"]}, {"$push": {f"{field_value}": new_element}})

    else:
        _id = ObjectId()
        db["logbook"].update_one(
            {"_id": ObjectId(_id)},
            {
                "$set": {
                    "date": date,
                    "creation_date": date,
                    "shift": shift,
                    "dayofweek": day_of_week,
                    "creation_user": ObjectId(get_current_user().uid),
                    f"{field}": [{"id": id, "notes": notes, "operator": ObjectId(get_current_user().uid)}],
                }
            },
            upsert=True,
        )
