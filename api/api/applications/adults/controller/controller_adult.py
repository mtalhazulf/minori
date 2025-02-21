from datetime import datetime, timedelta

from bson import ObjectId
from flask import jsonify
from werkzeug.exceptions import BadRequest

from api.applications.adults.helper.adult import edit_adult, update_adult
from api.applications.adults.helper.attendance import check_attendance
from api.applications.adults.helper.price import (
    calcola_ricavi_tra_date,
    calculate_intersection,
)
from api.applications.tasks.helper.medication import queryParams
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo
from api.utils.session import get_current_user


def adults_adult_get(name, surname, fiscal_code, entry_date, status, page=0, limit=8):
    data = {
        "name": name,
        "surname": surname,
        "fiscal_code": fiscal_code,
    }
    query = queryParams(data)

    db = get_mongo().cx.get_default_database()
    if status == "enabled" or status == "":
        query = [
            {"$or": [{"status": "enabled"}, {"status": {"$exists": False}}]},
            query,
        ]
    if status == "disabled":
        query = [
            {"$or": [{"status": "disabled"}]},
            query,
        ]
    records = list(db["adults"].find({"$and": query}))
    for record in records:
        if "deactivation_date" in record:
            record["deactivation_date"] = record["deactivation_date"].strftime("%Y-%m-%d %H:%M")

    filtered_records = []
    if entry_date:
        entry_date_object = datetime.strptime(entry_date, "%d/%m/%Y")
        for record in records:
            if record.get("info_sheet") and record["info_sheet"]["adult"].get("entry_date"):
                record_entry_date = datetime.strptime(record["info_sheet"]["adult"]["entry_date"], "%d/%m/%Y")
                if record_entry_date >= entry_date_object:
                    filtered_records.append(record)
    else:
        filtered_records = records

    total_records = len(filtered_records)
    paginated_results = filtered_records[page * limit : (page + 1) * limit]

    return jsonify_mongo(
        {
            "paginatedResults": paginated_results,
            "meta": {"rowsNumber": total_records, "page": page + 1, "rowsPerPage": limit},
        }
    )


def adults_adult_all_get():
    db = get_mongo().cx.get_default_database()
    query = {"$or": [{"status": "enabled"}, {"status": {"$exists": False}}]}
    results = list(db["adults"].find(query))
    return jsonify_mongo(results)


# TODO: Add filter on disposal date (where not exists or disposal_date between start_date and end_date
def adults_adult_present_get(start_date, end_date):
    db = get_mongo().cx.get_default_database()
    return jsonify_mongo(db["adults"].find())


def adults_adult_present_prices_get(start_date, end_date):
    db = get_mongo().cx.get_default_database()
    adults = db["adults"].find()
    adults_list = list(adults)
    for adult in adults_list:
        adult_price = db["adultPrice"].find_one({"adult_id": adult.get("_id")})
        if adult_price:
            entry_date = adult["info_sheet"]["adult"]["entry_date"] if "info_sheet" in adult else None
            disposal_date = adult["info_sheet"]["adult"]["disposal_date"] if "info_sheet" in adult else None
            adult["entry_date"] = entry_date
            adult["disposal_date"] = disposal_date
            intersection_start, intersection_end, intersection_days = calculate_intersection(
                start_date, end_date, entry_date, disposal_date
            )
            total_price = calcola_ricavi_tra_date(
                data_inizio=intersection_start, data_fine=intersection_end - timedelta(days=1), adult_price=adult_price
            )
            # adult["price"] = str(adult_price.get("value"))
            history_ordinata = sorted(
                adult_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d")
            )
            adult_price["history"] = history_ordinata
            adult["price"] = adult_price
            adult["total_price"] = total_price
            adult["attendances"] = intersection_days
        else:
            adult["price"] = None
            adult["total_price"] = None
            adult["attendances"] = None

    return jsonify_mongo(adults_list)


def adults_adult_arg_get(arg):
    db = get_mongo().cx.get_default_database()
    return jsonify_mongo(db["adults"].find_one({"_id": ObjectId(arg)}))


def adults_adult_arg_put(arg, body):
    db = get_mongo().cx.get_default_database()

    if db["adults"].find_one({"_id": ObjectId(arg)}):
        return edit_adult(db, arg, body)
    else:
        attendance = db["adultAttendance"].find_one({"_id": ObjectId(arg)})
        if attendance:
            return edit_adult(db, attendance["adultId"], body)
        else:
            raise BadRequest("Adulto non esiste")


def adults_adult_disable_arg_put(arg):
    db = get_mongo().cx.get_default_database()
    now = datetime.now()
    if db["adults"].find_one({"_id": ObjectId(arg)}):
        return update_adult(db, arg, now)
    # else:
    #     attendance = db["adultAttendance"].find_one({"_id": ObjectId(arg)})
    #     if attendance:
    #         remove_attendance(db, arg)
    #         return update_adult(db, attendance["adultId"])
    else:
        raise BadRequest("Adulto non esiste")


def adults_adult_post(body):
    db = get_mongo().cx.get_default_database()
    if "fiscal_code" in body and db["adults"].find_one(
        {
            "$and": [
                {"fiscal_code": body["fiscal_code"]},
                {"fiscal_code": {"$exists": True}},
                {"$or": [{"status": "enabled"}, {"status": {"$exists": False}}]},
            ]
        }
    ):
        return {"success": False, "msg": "Il codice fiscale inserito è già in uso"}
    elif db["adults"].find_one(
        {
            "name": body["name"],
            "surname": body["surname"],
            "$or": [{"status": "enabled"}, {"status": {"$exists": False}}],
        }
    ):
        return {
            "success": False,
            "msg": "Nome e cognome già in uso, si prega di specificare il codice fiscale se si vuole ugualmente "
            "inserire il adulto.",
        }
    else:
        _id = ObjectId()
        today = datetime.now()
        db["adults"].update_one(
            {"_id": ObjectId(_id)},
            {
                "$set": {
                    **body,
                    "creation_date": today,
                    "creation_user": ObjectId(get_current_user().uid),
                }
            },
            upsert=True,
        )
        check_attendance(db, _id, body)
        return jsonify({"success": True})


def adults_adult_arg_post(arg, body):
    db = get_mongo().cx.get_default_database()
    today = datetime.now()
    body["creation_date"] = today
    body["creationUser"] = ObjectId(get_current_user().uid)
    adult = db["adults"].find_one({"_id": ObjectId(arg)})
    if adult:
        if adult.get("info_sheet"):
            amount_euro_body = body.get("adult").get("amount_euro")
            if amount_euro_body and float(amount_euro_body) > 0:
                result = db["adults"].update_one(
                    {"_id": ObjectId(arg)},
                    {"$set": {"info_sheet": body, "modified": "true"}},
                )
            else:
                result = db["adults"].update_one(
                    {"_id": ObjectId(arg)},
                    {"$set": {"info_sheet": body}},
                )
        else:
            amount_euro_body = body.get("adult").get("amount_euro")
            if amount_euro_body and float(amount_euro_body) > 0:
                result = db["adults"].update_one(
                    {"_id": ObjectId(arg)},
                    {"$set": {"info_sheet": body, "modified": "true"}},
                )
            else:
                result = db["adults"].update_one(
                    {"_id": ObjectId(arg)},
                    {"$set": {"info_sheet": body, "modified": "false"}},
                )
        if result.matched_count == 0:
            raise BadRequest("Adulto non esiste")
        else:
            return jsonify({"success": True})
    else:
        raise BadRequest("Adulto non esiste")
