from datetime import datetime, timedelta

from bson import ObjectId

# def get_shifts(db, data):
#     data["date"] = datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(day=1)
#     start_date = datetime.combine(data["date"].date(), datetime.min.time())
#     end_date = start_date.replace(month=1 if start_date.month == 12 else start_date.month + 1)
#     shifts = list(db["shifts"].find({"date": {"$gte": start_date, "$lte": end_date}}))

#     return shifts


def get_shifts_with_cost(db, data):
    data["date"] = datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(day=1)
    start_date = datetime.combine(data["date"].date(), datetime.min.time())
    end_date = start_date.replace(month=1 if start_date.month == 12 else start_date.month + 1)
    shifts = list(db["shifts"].find({"date": {"$gte": start_date, "$lte": end_date}}))

    operator_hours = {}
    for shift in shifts:
        operator_id = shift.get("operatorId")
        if operator_id:
            start_time = shift["startTime"]
            end_time = shift["endTime"]

            if isinstance(start_time, str):
                start_time = datetime.strptime(start_time, "%H:%M").time()
            elif isinstance(start_time, datetime):
                start_time = start_time.time()

            if isinstance(end_time, str):
                end_time = datetime.strptime(end_time, "%H:%M").time()
            elif isinstance(end_time, datetime):
                end_time = end_time.time()

            # Convert operatorId to string if it's an ObjectId
            operator_id = (
                str(operator_id["$oid"])
                if isinstance(operator_id, dict) and "$oid" in operator_id
                else str(operator_id)
            )
            hours = calculate_hours(start_time, end_time)
            operator_hours[operator_id] = operator_hours.get(operator_id, 0) + hours

    result = []
    for operator_id, total_hours in operator_hours.items():
        user = db["users"].find_one({"_id": ObjectId(operator_id)})
        if user:
            hourly_cost = float(user.get("hourly_cost", 0))
            total_cost = total_hours * hourly_cost
            result.append(
                {
                    "operator_id": operator_id,
                    "name": f"{user.get('name', '')} {user.get('surname', '')}",
                    "email": user.get("email"),
                    "total_hours": round(total_hours, 2),
                    "hourly_cost": hourly_cost,
                    "total_cost": round(total_cost, 2),
                }
            )

    return {"shifts": shifts, "operator_costs": result}


def get_shifts_for_operator(db, operator_id, start_date, end_date):
    shifts = list(
        db["shifts"]
        .find({"operatorId": ObjectId(operator_id), "date": {"$gte": start_date, "$lt": end_date}})
        .sort("date", 1)
    )

    user = db["users"].find_one({"_id": ObjectId(operator_id)})
    hourly_cost = float(user.get("hourly_cost", 0))

    total_hours = 0
    total_cost = 0

    for shift in shifts:
        start_time = shift["startTime"]
        end_time = shift["endTime"]

        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M").time()
        elif isinstance(start_time, datetime):
            start_time = start_time.time()

        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M").time()
        elif isinstance(end_time, datetime):
            end_time = end_time.time()

        hours = calculate_hours(start_time, end_time)
        total_hours += hours
        total_cost += hours * hourly_cost

    return {
        "shifts": shifts,
        "operator_summary": {
            "operator_id": str(operator_id),
            "name": f"{user.get('name', '')} {user.get('surname', '')}",
            "email": user.get("email"),
            "total_hours": round(total_hours, 2),
            "hourly_cost": hourly_cost,
            "total_cost": round(total_cost, 2),
        },
    }


def calculate_hours(start_time, end_time):
    # Convert time objects to timedelta for calculation
    start_delta = timedelta(hours=start_time.hour, minutes=start_time.minute)
    end_delta = timedelta(hours=end_time.hour, minutes=end_time.minute)

    # If end time is earlier than start time, assume it's the next day
    if end_delta <= start_delta:
        end_delta += timedelta(days=1)

    # Calculate the difference
    duration = end_delta - start_delta
    return duration.total_seconds() / 3600


def get_operator_shifts(db, operator_id, start_date=None, end_date=None):
    # If no dates provided, default to current month
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = (start_date + timedelta(days=31)).replace(day=1)

    # Query shifts for the specific operator within the date range
    shifts = list(db["shifts"].find({"operatorId": operator_id, "date": {"$gte": start_date, "$lt": end_date}}))

    # Process shifts (similar to get_shifts function)
    for shift in shifts:
        shift["date"] = shift["date"].strftime("%Y-%m-%d")
        shift["startTime"] = shift["startTime"].strftime("%H:%M")
        shift["endTime"] = shift["endTime"].strftime("%H:%M")

        start_datetime = datetime.combine(shift["date"], datetime.strptime(shift["startTime"], "%H:%M").time())
        end_datetime = datetime.combine(shift["date"], datetime.strptime(shift["endTime"], "%H:%M").time())
        shift["duration"] = str(end_datetime - start_datetime)

        shift["_id"] = str(shift["_id"])
        shift["operatorId"] = str(shift["operatorId"])

    return shifts


# def update_monthly_cost(db, shift, cost):
#     month_start = shift['date'].replace(day=1)
#     year = month_start.year
#     month = month_start.month

#     update_result = db['monthly_costs'].update_one(
#         {
#             'year': year,
#             'month': month
#         },
#         {
#             '$inc': {
#                 'total_hours': (shift["endTime"] - shift["startTime"]).total_seconds() / 3600,
#                 'total_cost': cost
#             },
#             '$push': {
#                 'operator_costs': {
#                     'operatorId': shift['operatorId'],
#                     'hours': (shift["endTime"] - shift["startTime"]).total_seconds() / 3600,
#                     'cost': cost
#                 }
#             },
#             '$setOnInsert': {
#                 'createdAt': datetime.now(),
#                 'extra_costs': []
#             },
#             '$set': {
#                 'updatedAt': datetime.now()
#             }
#         },
#         upsert=True
#     )

#     return update_result


def update_monthly_cost(db, shift, cost):
    month_start = shift["date"].replace(day=1)
    year = month_start.year
    month = month_start.month

    hours = (shift["endTime"] - shift["startTime"]).total_seconds() / 3600

    update_result = db["monthly_costs"].update_one(
        {"year": year, "month": month},
        {
            "$inc": {"total_hours": hours, "total_cost": cost},
            "$push": {"operator_costs": {"operatorId": shift["operatorId"], "hours": hours, "cost": cost}},
            "$setOnInsert": {"createdAt": datetime.now(), "extra_costs": []},
            "$set": {"updatedAt": datetime.now()},
        },
        upsert=True,
    )

    return update_result


def add_extra_cost(db, year, month, item_name, cost):
    update_result = db["monthly_costs"].update_one(
        {"year": year, "month": month},
        {
            "$push": {"extra_costs": {"item_name": item_name, "cost": cost}},
            "$inc": {"total_cost": cost},
            "$set": {"updatedAt": datetime.now()},
        },
        upsert=True,
    )

    return update_result


def update_extra_cost(db, year, month, operator_id, extra_cost):
    db["monthly_costs"].update_one(
        {"year": year, "month": month, "operatorId": ObjectId(operator_id)},
        {"$set": {"extra_cost": extra_cost, "updatedAt": datetime.now()}},
        upsert=True,
    )


def delete_extra_cost(db, year, month, item_name, cost):
    result = db["monthly_costs"].update_one(
        {"year": year, "month": month},
        {
            "$pull": {"extra_costs": {"item_name": item_name, "cost": cost}},
            "$inc": {"total_cost": -cost},
            "$set": {"updatedAt": datetime.now()},
        },
    )
    return result.modified_count > 0


def calculate_shift_cost(db, shift):
    operator = db["users"].find_one({"_id": shift["operatorId"]})
    hourly_rate = float(operator.get("hourly_cost", 0))
    duration = (shift["endTime"] - shift["startTime"]).total_seconds() / 3600  # Convert to hours
    return round(duration * hourly_rate, 2)


def get_monthly_cost(db, year, month):
    monthly_cost = db["monthly_costs"].find_one({"year": year, "month": month})

    if monthly_cost:
        # Convert ObjectIds to strings for JSON serialization
        monthly_cost["_id"] = str(monthly_cost["_id"])
        for op_cost in monthly_cost.get("operator_costs", []):
            op_cost["operatorId"] = str(op_cost["operatorId"])

    return monthly_cost
