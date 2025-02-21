from datetime import datetime

from bson import ObjectId
from flask import jsonify

from api.applications.minors.helper.price import calcola_ricavi_tra_date
from api.middleware.mongo import get_mongo


def minors_minor_price_get():
    db = get_mongo().cx.get_default_database()
    results = list(db["minorPrice"].find())
    for minor_price in results:
        history_ordinata = sorted(
            minor_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d"), reverse=True
        )
        minor_price["history"] = history_ordinata
    return results


def minors_minor_id_price_post(id, body):
    db = get_mongo().cx.get_default_database()
    value = body.get("value")
    timestamp = body.get("timestamp")
    minor = db["children"].find_one({"_id": ObjectId(id)})
    minor_price = db["minorPrice"].find_one({"children_id": ObjectId(id)})
    if not minor:
        return jsonify({"success": False, "message": "Minor not found."}), 404
    elif minor_price:
        result = db["minorPrice"].find_one({"children_id": ObjectId(id), "history.timestamp": timestamp})
        if not result:
            history_ordinata = sorted(
                minor_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d")
            )
            if history_ordinata[-1]["timestamp"] < timestamp:
                result = db["minorPrice"].update_one(
                    {"children_id": ObjectId(id)},
                    {"$set": {"value": value}, "$push": {"history": {"value": value, "timestamp": timestamp}}},
                )
            else:
                result = db["minorPrice"].update_one(
                    {"children_id": ObjectId(id)},
                    {"$push": {"history": {"value": value, "timestamp": timestamp}}},
                )
            if result.matched_count > 0:
                return jsonify({"success": True, "message": "Price to minor successfully added."}), 200
            else:
                return jsonify({"success": False, "message": "Error in adding price to minor."}), 404
        else:
            return jsonify({"success": False, "message": "Date for minor already present"}), 404
    else:
        result = (
            db["minorPrice"]
            .insert_one(
                {"children_id": ObjectId(id), "value": value, "history": [{"value": value, "timestamp": timestamp}]}
            )
            .inserted_id
        )
        if result:
            return jsonify({"success": True, "message": "Price to minor successfully added."}), 200
        else:
            return jsonify({"success": False, "message": "Error in adding price to minor."}), 404


def minors_minor_id_price_get(id):
    db = get_mongo().cx.get_default_database()
    minor_price = db["minorPrice"].find_one({"children_id": ObjectId(id)})
    if minor_price:
        history_ordinata = sorted(
            minor_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d"), reverse=True
        )
        minor_price["history"] = history_ordinata
        return jsonify(minor_price)
    else:
        return jsonify({"success": False, "message": "Minorprice not found."}), 404


def minors_minor_id_price_timestamp_delete(id, timestamp):
    db = get_mongo().cx.get_default_database()
    minor_price = db["minorPrice"].find_one({"children_id": ObjectId(id)})
    if minor_price:
        history_ordinata = sorted(minor_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d"))
        if history_ordinata[-1]["timestamp"] == timestamp:
            result = db["minorPrice"].update_one(
                {"children_id": ObjectId(id)}, {"$pull": {"history": {"timestamp": timestamp}}}
            )
            if result.modified_count > 0:
                history_ordinata.pop()
                if len(history_ordinata) != 0:
                    db["minorPrice"].update_one(
                        {"children_id": ObjectId(id)}, {"$set": {"value": history_ordinata[-1]["value"]}}
                    )
                else:
                    db["minorPrice"].delete_one({"children_id": ObjectId(id)})
        else:
            result = db["minorPrice"].update_one(
                {"children_id": ObjectId(id)}, {"$pull": {"history": {"timestamp": timestamp}}}
            )
        if result.modified_count > 0:
            return jsonify({"success": True, "message": "Elemento di history cancellato con successo"})
        else:
            return jsonify({"success": False, "message": "Minorprice or timestamp not found"}), 404
    else:
        return jsonify({"success": False, "message": "Minorprice not found"}), 404


def minors_minor_id_price_timestamp_patch(id, timestamp, body):
    db = get_mongo().cx.get_default_database()
    minor_price = db["minorPrice"].find_one({"children_id": ObjectId(id)})
    if minor_price:
        history_ordinata = sorted(minor_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d"))
        if history_ordinata[-1]["timestamp"] == timestamp:
            result = db["minorPrice"].update_one(
                {"children_id": ObjectId(id), "history.timestamp": timestamp},
                {"$set": {"value": body.get("value"), "history.$.value": body.get("value")}},
            )
        else:
            result = db["minorPrice"].update_one(
                {"children_id": ObjectId(id), "history.timestamp": timestamp},
                {"$set": {"history.$.value": body.get("value")}},
            )
        if result.modified_count > 0:
            return jsonify({"success": True, "message": "Value for given children_id and timestamp patched"})
        else:
            return jsonify({"success": False, "message": "Timestamp not found"}), 404
    else:
        return jsonify({"success": False, "message": "Minorprice not found"}), 404


def minors_minor_id_calculate_get(id, start_date, end_date):
    db = get_mongo().cx.get_default_database()
    minor_price = db["minorPrice"].find_one({"children_id": ObjectId(id)})
    if minor_price:
        return jsonify(calcola_ricavi_tra_date(data_inizio=start_date, data_fine=end_date, minor_price=minor_price))
    else:
        return jsonify({"success": False, "message": "Minor not found."}), 404
