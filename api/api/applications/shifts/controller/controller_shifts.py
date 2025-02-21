from datetime import datetime, timedelta

from bson import ObjectId
from flask import jsonify, request

from api.applications.shifts.helper.shift import (
    add_extra_cost,
    calculate_shift_cost,
    delete_extra_cost,
    get_monthly_cost,
    get_shifts_for_operator,
    get_shifts_with_cost,
    update_extra_cost,
    update_monthly_cost,
)
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo


def shifts_get():
    db = get_mongo().cx.get_default_database()
    if request.args and "date" in request.args.to_dict():
        return jsonify_mongo(get_shifts_with_cost(db, request.args.to_dict()))
    # You might want to implement a default behavior if no start_date is provided

    if "operatorId" in request.args and "start" in request.args and "end" in request.args:
        operator_id = request.args["operatorId"]
        start_date = datetime.fromisoformat(request.args["start"].replace("Z", "+00:00"))
        end_date = datetime.fromisoformat(request.args["end"].replace("Z", "+00:00"))

        return jsonify_mongo(get_shifts_for_operator(db, operator_id, start_date, end_date))

    return jsonify_mongo(get_shifts_with_cost(db, {}))


def shifts_upcoming_get():
    db = get_mongo().cx.get_default_database()
    now = datetime.now()
    upcoming_date = now + timedelta(days=7)  # Get shifts for the next 7 days
    shifts = list(db["shifts"].find({"date": {"$gte": now, "$lte": upcoming_date}}))
    return jsonify(count=len(shifts), upcoming=True if len(shifts) > 0 else False)


# def shifts_post(body):
#     db = get_mongo().cx.get_default_database()
#     _id = ObjectId()
#     today = datetime.now()
#     if "operatorId" in body:
#         body["operatorId"] = ObjectId(body["operatorId"])

#     body["date"] = datetime.strptime(body["date"], "%d/%m/%Y")

#     start_time = datetime.strptime(body["startTime"], "%H:%M").time()
#     end_time = datetime.strptime(body["endTime"], "%H:%M").time()
#     body["startTime"] = datetime.combine(body["date"], start_time)
#     body["endTime"] = datetime.combine(body["date"], end_time)

#     db["shifts"].update_one(
#         {"_id": ObjectId(_id)},
#         {"$set": {**body, "createdAt": today, "updatedAt": today}},
#         upsert=True,
#     )

#     shift_cost = calculate_shift_cost(db, body)
#     update_monthly_cost(db, body, shift_cost)

#     return {"success": True}


def shifts_post(body):
    db = get_mongo().cx.get_default_database()
    _id = ObjectId()
    today = datetime.now()
    if "operatorId" in body:
        body["operatorId"] = ObjectId(body["operatorId"])

    body["date"] = datetime.strptime(body["date"], "%d/%m/%Y")

    start_time = datetime.strptime(body["startTime"], "%H:%M").time()
    end_time = datetime.strptime(body["endTime"], "%H:%M").time()
    body["startTime"] = datetime.combine(body["date"], start_time)
    body["endTime"] = datetime.combine(body["date"], end_time)

    db["shifts"].update_one(
        {"_id": ObjectId(_id)},
        {"$set": {**body, "createdAt": today, "updatedAt": today}},
        upsert=True,
    )

    shift_cost = calculate_shift_cost(db, body)
    update_monthly_cost(db, body, shift_cost)

    return {"success": True}


# def shifts_put(shift_id, body):
#     db = get_mongo().cx.get_default_database()
#     if "operatorId" in body:
#         body["operatorId"] = ObjectId(body["operatorId"])
#     if "date" in body:
#         body["date"] = datetime.strptime(body["date"], "%d/%m/%Y")
#     if "startTime" in body:
#         body["startTime"] = datetime.strptime(body["startTime"], "%H:%M").time().strftime("%H:%M")
#     if "endTime" in body:
#         body["endTime"] = datetime.strptime(body["endTime"], "%H:%M").time().strftime("%H:%M")
#     body["updatedAt"] = datetime.now()
#     result = db["shifts"].update_one(
#         {"_id": ObjectId(shift_id)},
#         {"$set": body}
#     )

#     if result.modified_count > 0:
#         # Remove old shift cost from monthly cost
#         old_cost = calculate_shift_cost(db, old_shift)
#         update_monthly_cost(db, old_shift, -old_cost)

#         # Add new shift cost to monthly cost
#         new_shift = db["shifts"].find_one({"_id": ObjectId(shift_id)})
#         new_cost = calculate_shift_cost(db, new_shift)
#         update_monthly_cost(db, new_shift, new_cost)


#     return {"success": True if result.modified_count > 0 else False}
def shifts_put(shift_id, body):
    db = get_mongo().cx.get_default_database()
    old_shift = db["shifts"].find_one({"_id": ObjectId(shift_id)})
    if not old_shift:
        return {"success": False, "error": "Shift not found"}, 404

    if "operatorId" in body:
        body["operatorId"] = ObjectId(body["operatorId"])
    if "date" in body:
        body["date"] = datetime.strptime(body["date"], "%d/%m/%Y")
    if "startTime" in body:
        body["startTime"] = datetime.strptime(body["startTime"], "%H:%M")
    if "endTime" in body:
        body["endTime"] = datetime.strptime(body["endTime"], "%H:%M")
    body["updatedAt"] = datetime.now()

    result = db["shifts"].update_one({"_id": ObjectId(shift_id)}, {"$set": body})

    if result.modified_count > 0:
        # Remove old shift cost from monthly cost
        old_cost = calculate_shift_cost(db, old_shift)
        update_monthly_cost(db, old_shift, -old_cost)

        # Add new shift cost to monthly cost
        new_shift = db["shifts"].find_one({"_id": ObjectId(shift_id)})
        new_cost = calculate_shift_cost(db, new_shift)
        update_monthly_cost(db, new_shift, new_cost)

    return {"success": True if result.modified_count > 0 else False}


def shifts_delete(shift_id):
    db = get_mongo().cx.get_default_database()
    shift = db["shifts"].find_one({"_id": ObjectId(shift_id)})
    if shift:
        cost = calculate_shift_cost(db, shift)
        update_monthly_cost(db, shift, -cost)  # Remove the cost from monthly total

    result = db["shifts"].delete_one({"_id": ObjectId(shift_id)})

    return {"success": True if result.deleted_count > 0 else False}


def update_operator_extra_cost(db, year, month, operator_id, extra_cost):
    update_extra_cost(db, year, month, operator_id, extra_cost)
    return {"success": True}


def get_monthly_cost_endpoint():
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))
    db = get_mongo().cx.get_default_database()
    monthly_cost = get_monthly_cost(db, year, month)
    return jsonify(monthly_cost)


def shifts_extra_costs_post():
    db = get_mongo().cx.get_default_database()
    data = request.json
    year = data.get("year")
    month = data.get("month")
    item_name = data.get("item_name")
    cost = data.get("cost")

    if not all([year, month, item_name, cost]):
        return jsonify({"error": "Missing required fields"}), 400

    result = add_extra_cost(db, year, month, item_name, cost)
    return jsonify({"success": True, "result": str(result.upserted_id)})


def shifts_extra_costs_get():
    db = get_mongo().cx.get_default_database()
    year = request.args.get("year")
    month = request.args.get("month")

    if not year or not month:
        return jsonify({"error": "Year and month are required"}), 400

    monthly_cost = db["monthly_costs"].find_one({"year": int(year), "month": int(month)})

    extra_costs = monthly_cost.get("extra_costs", []) if monthly_cost else []
    total_extra_cost = sum(item["cost"] for item in extra_costs)
    total_cost = monthly_cost.get("total_cost", 0) if monthly_cost else 0

    return jsonify({"extra_costs": extra_costs, "total_extra_cost": total_extra_cost, "total_cost": total_cost})


def shifts_extra_costs_delete():
    db = get_mongo().cx.get_default_database()
    data = request.json
    year = data.get("year")
    month = data.get("month")
    item_name = data.get("item_name")
    cost = data.get("cost")

    if not all([year, month, item_name, cost]):
        return jsonify({"error": "Missing required fields"}), 400

    success = delete_extra_cost(db, int(year), int(month), item_name, float(cost))
    if success:
        return jsonify({"success": True, "message": "Extra cost deleted successfully"})
    else:
        return jsonify({"success": False, "message": "Extra cost not found or could not be deleted"}), 404
