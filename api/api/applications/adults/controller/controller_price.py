from datetime import datetime

from bson import ObjectId
from flask import jsonify

from api.applications.adults.helper.price import calcola_ricavi_tra_date
from api.middleware.mongo import get_mongo


def adults_adult_price_get():
    db = get_mongo().cx.get_default_database()
    results = list(db["adultPrice"].find())
    for adult_price in results:
        history_ordinata = sorted(
            adult_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d"), reverse=True
        )
        adult_price["history"] = history_ordinata
    return results


def adults_adult_id_price_post(id, body):
    db = get_mongo().cx.get_default_database()
    value = body.get("value")
    timestamp = body.get("timestamp")
    adult = db["adults"].find_one({"_id": ObjectId(id)})
    adult_price = db["adultPrice"].find_one({"adult_id": ObjectId(id)})
    if not adult:
        return jsonify({"success": False, "message": "Adult not found."}), 404
    elif adult_price:
        result = db["adultPrice"].find_one({"adult_id": ObjectId(id), "history.timestamp": timestamp})
        if not result:
            history_ordinata = sorted(
                adult_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d")
            )
            if history_ordinata[-1]["timestamp"] < timestamp:
                result = db["adultPrice"].update_one(
                    {"adult_id": ObjectId(id)},
                    {"$set": {"value": value}, "$push": {"history": {"value": value, "timestamp": timestamp}}},
                )
            else:
                result = db["adultPrice"].update_one(
                    {"adult_id": ObjectId(id)},
                    {"$push": {"history": {"value": value, "timestamp": timestamp}}},
                )
            if result.matched_count > 0:
                return jsonify({"success": True, "message": "Price to adult successfully added."}), 200
            else:
                return jsonify({"success": False, "message": "Error in adding price to adult."}), 404
        else:
            return jsonify({"success": False, "message": "Date for adult already present"}), 404
    else:
        result = (
            db["adultPrice"]
            .insert_one(
                {"adult_id": ObjectId(id), "value": value, "history": [{"value": value, "timestamp": timestamp}]}
            )
            .inserted_id
        )
        if result:
            return jsonify({"success": True, "message": "Price to adult successfully added."}), 200
        else:
            return jsonify({"success": False, "message": "Error in adding price to adult."}), 404


def adults_adult_id_price_get(id):
    db = get_mongo().cx.get_default_database()
    adult_price = db["adultPrice"].find_one({"adult_id": ObjectId(id)})
    if adult_price:
        history_ordinata = sorted(
            adult_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d"), reverse=True
        )
        adult_price["history"] = history_ordinata
        return jsonify(adult_price)
    else:
        return jsonify({"success": False, "message": "Adultprice not found."}), 404


def adults_adult_id_price_timestamp_delete(id, timestamp):
    db = get_mongo().cx.get_default_database()
    adult_price = db["adultPrice"].find_one({"adult_id": ObjectId(id)})
    if adult_price:
        history_ordinata = sorted(adult_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d"))
        if history_ordinata[-1]["timestamp"] == timestamp:
            result = db["adultPrice"].update_one(
                {"adult_id": ObjectId(id)}, {"$pull": {"history": {"timestamp": timestamp}}}
            )
            if result.modified_count > 0:
                history_ordinata.pop()
                if len(history_ordinata) != 0:
                    db["adultPrice"].update_one(
                        {"adult_id": ObjectId(id)}, {"$set": {"value": history_ordinata[-1]["value"]}}
                    )
                else:
                    db["adultPrice"].delete_one({"adult_id": ObjectId(id)})
        else:
            result = db["adultPrice"].update_one(
                {"adult_id": ObjectId(id)}, {"$pull": {"history": {"timestamp": timestamp}}}
            )
        if result.modified_count > 0:
            return jsonify({"success": True, "message": "Elemento di history cancellato con successo"})
        else:
            return jsonify({"success": False, "message": "Adultprice or timestamp not found"}), 404
    else:
        return jsonify({"success": False, "message": "Adultprice not found"}), 404


def adults_adult_id_price_timestamp_patch(id, timestamp, body):
    db = get_mongo().cx.get_default_database()
    adult_price = db["adultPrice"].find_one({"adult_id": ObjectId(id)})
    if adult_price:
        history_ordinata = sorted(adult_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d"))
        if history_ordinata[-1]["timestamp"] == timestamp:
            result = db["adultPrice"].update_one(
                {"adult_id": ObjectId(id), "history.timestamp": timestamp},
                {"$set": {"value": body.get("value"), "history.$.value": body.get("value")}},
            )
        else:
            result = db["adultPrice"].update_one(
                {"adult_id": ObjectId(id), "history.timestamp": timestamp},
                {"$set": {"history.$.value": body.get("value")}},
            )
        if result.modified_count > 0:
            return jsonify({"success": True, "message": "Value for given adult_id and timestamp patched"})
        else:
            return jsonify({"success": False, "message": "Timestamp not found"}), 404
    else:
        return jsonify({"success": False, "message": "Adultprice not found"}), 404


def adults_adult_id_calculate_get(id, start_date, end_date):
    db = get_mongo().cx.get_default_database()
    adult_price = db["adultPrice"].find_one({"adult_id": ObjectId(id)})
    if adult_price:
        return jsonify(calcola_ricavi_tra_date(data_inizio=start_date, data_fine=end_date, adult_price=adult_price))
    else:
        return jsonify({"success": False, "message": "Adult not found."}), 404
