from datetime import datetime, timedelta

from bson import ObjectId
from flask import jsonify
from werkzeug.exceptions import BadRequest

from api.applications.minors.helper.attendance import check_attendance
from api.applications.minors.helper.minor import (
    edit_minor,
    fetch_tasks_between_date_range,
    remove_empty_attributes,
    update_minor,
)
from api.applications.minors.helper.price import (
    calcola_ricavi_tra_date,
    calculate_intersection,
)
from api.applications.tasks.helper.medication import queryParams
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo
from api.utils.openai import summarize_info_sheet
from api.utils.session import get_current_user


def minors_minor_get(name, surname, fiscal_code, entry_date, status, page=0, limit=8):
    data = {"name": name, "surname": surname, "fiscal_code": fiscal_code}
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
    records = list(db["children"].find({"$and": query}))
    for record in records:
        if "deactivation_date" in record:
            record["deactivation_date"] = record["deactivation_date"].strftime("%Y-%m-%d %H:%M")

    filtered_records = []
    if entry_date:
        entry_date_object = datetime.strptime(entry_date, "%d/%m/%Y")
        for record in records:
            if "deactivation_date" in record:
                record["deactivation_date"] = record["deactivation_date"].strftime("%Y-%m-%d %H:%M")
            if record.get("info_sheet") and record["info_sheet"]["minor"].get("entry_date"):
                record_entry_date = datetime.strptime(record["info_sheet"]["minor"]["entry_date"], "%d/%m/%Y")
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


def minors_minor_all_get():
    db = get_mongo().cx.get_default_database()
    query = {"$or": [{"status": "enabled"}, {"status": {"$exists": False}}]}
    results = list(db["children"].find(query))
    return jsonify_mongo(results)


# TODO: Add filter on disposal date (where not exists or disposal_date between start_date and end_date
def minors_minor_present_get(start_date, end_date):
    db = get_mongo().cx.get_default_database()
    return jsonify_mongo(db["children"].find())


def minors_minor_present_prices_get(start_date, end_date):
    db = get_mongo().cx.get_default_database()
    minors = db["children"].find()
    minors_list = list(minors)
    for minor in minors_list:
        minor_price = db["minorPrice"].find_one({"children_id": minor.get("_id")})
        if minor_price:
            entry_date = minor["info_sheet"]["minor"]["entry_date"] if "info_sheet" in minor else None
            disposal_date = minor["info_sheet"]["minor"]["disposal_date"] if "info_sheet" in minor else None
            minor["entry_date"] = entry_date
            minor["disposal_date"] = disposal_date
            intersection_start, intersection_end, intersection_days = calculate_intersection(
                start_date, end_date, entry_date, disposal_date
            )
            total_price = calcola_ricavi_tra_date(
                data_inizio=intersection_start, data_fine=intersection_end - timedelta(days=1), minor_price=minor_price
            )
            # minor["price"] = str(minor_price.get("value"))
            history_ordinata = sorted(
                minor_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d")
            )
            minor_price["history"] = history_ordinata
            minor["price"] = minor_price
            minor["total_price"] = total_price
            minor["attendances"] = intersection_days
        else:
            minor["price"] = None
            minor["total_price"] = None
            minor["attendances"] = None

    return jsonify_mongo(minors_list)


def minors_minor_arg_get(arg):
    db = get_mongo().cx.get_default_database()
    return jsonify_mongo(db["children"].find_one({"_id": ObjectId(arg)}))


def minors_minor_arg_put(arg, body):
    db = get_mongo().cx.get_default_database()

    if db["children"].find_one({"_id": ObjectId(arg)}):
        return edit_minor(db, arg, body)
    else:
        attendance = db["minorAttendance"].find_one({"_id": ObjectId(arg)})
        if attendance:
            return edit_minor(db, attendance["minorId"], body)
        else:
            raise BadRequest("Minore non esiste")


def minors_minor_disable_arg_put(arg):
    db = get_mongo().cx.get_default_database()
    now = datetime.now()
    if db["children"].find_one({"_id": ObjectId(arg)}):
        return update_minor(db, arg, now)
    # else:
    #     attendance = db["minorAttendance"].find_one({"_id": ObjectId(arg)})
    #     if attendance:
    #         remove_attendance(db, arg)
    #         return update_minor(db, attendance["minorId"], now)
    else:
        raise BadRequest("Minore non esiste")


def minors_minor_post(body):
    db = get_mongo().cx.get_default_database()
    if "fiscal_code" in body and db["children"].find_one(
        {
            "$and": [
                {"fiscal_code": body["fiscal_code"]},
                {"fiscal_code": {"$exists": True}},
                {"$or": [{"status": "enabled"}, {"status": {"$exists": False}}]},
            ]
        }
    ):
        return {"success": False, "msg": "Il codice fiscale inserito è già in uso"}
    elif db["children"].find_one(
        {
            "name": body["name"],
            "surname": body["surname"],
            "$or": [{"status": "enabled"}, {"status": {"$exists": False}}],
        }
    ):
        return {
            "success": False,
            "msg": "Nome e cognome già in uso, si prega di specificare il codice fiscale se si vuole ugualmente "
            "inserire il minore.",
        }
    else:
        _id = ObjectId()
        today = datetime.now()
        db["children"].update_one(
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


def minors_minor_arg_post(arg, body):
    db = get_mongo().cx.get_default_database()
    today = datetime.now()
    body["creation_date"] = today
    body["creationUser"] = ObjectId(get_current_user().uid)
    children = db["children"].find_one({"_id": ObjectId(arg)})
    if children:
        if children.get("info_sheet"):
            amount_euro_body = body.get("minor").get("amount_euro")
            if amount_euro_body and float(amount_euro_body) > 0:
                result = db["children"].update_one(
                    {"_id": ObjectId(arg)},
                    {"$set": {"info_sheet": body, "modified": "true"}},
                )
            else:
                result = db["children"].update_one(
                    {"_id": ObjectId(arg)},
                    {"$set": {"info_sheet": body}},
                )
        else:
            amount_euro_body = body.get("minor").get("amount_euro")
            if amount_euro_body and float(amount_euro_body) > 0:
                result = db["children"].update_one(
                    {"_id": ObjectId(arg)},
                    {"$set": {"info_sheet": body, "modified": "true"}},
                )
            else:
                result = db["children"].update_one(
                    {"_id": ObjectId(arg)},
                    {"$set": {"info_sheet": body, "modified": "false"}},
                )
        if result.matched_count == 0:
            raise BadRequest("Minore non esiste")
        else:
            return jsonify({"success": True})
    else:
        raise BadRequest("Minore non esiste")


def minors_minor_generate_summary_post(body):
    body["info_sheet"] = remove_empty_attributes(body["info_sheet"])
    body["start_date"]
    body["end_date"]
    db = get_mongo().cx.get_default_database()
    logs = fetch_tasks_between_date_range(db, body)
    summary = summarize_info_sheet(logs)
    return jsonify({"success": True, "summary": summary})
