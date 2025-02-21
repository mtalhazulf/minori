import math
from datetime import datetime

from bson import ObjectId
from flask import jsonify, request

from api.middleware.mongo import get_mongo
from api.utils.session import get_current_user


def rooms_room_post():
    db = get_mongo().cx.get_default_database()
    body = request.json
    guest_ids = body.get("guests", [])
    guest_ids = [ObjectId(guest_id) for guest_id in guest_ids]
    if len(guest_ids) > body["seats"]["total"]:
        return jsonify({"success": False, "message": "number of guests greater than total seats"}), 409
    children_count = db["children"].count_documents({"_id": {"$in": guest_ids}})
    if children_count != len(guest_ids):
        return (
            jsonify(
                {"success": False, "message": "One of more of the guests id are not present in children collection."}
            ),
            404,
        )

    occupied_seats = len(guest_ids)
    body["seats"]["occupied"] = occupied_seats
    available_seats = body["seats"]["total"] - occupied_seats
    body["seats"]["available"] = available_seats
    today = datetime.now()
    room = {**body, "creation_date": today, "creation_user": ObjectId(get_current_user().uid)}
    result = db["rooms"].insert_one(room)
    try:
        if result.inserted_id:
            return (
                jsonify(
                    {"success": True, "message": "Room created successfully.", "inserted_id": str(result.inserted_id)}
                ),
                201,
            )
        else:
            return jsonify({"success": False, "message": "Problem during creation of the room"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def rooms_room_get():
    db = get_mongo().cx.get_default_database()

    page = int(request.args.get("page")) if request.args.get("page") is not None else None
    limit = int(request.args.get("limit")) if request.args.get("limit") is not None else None

    room_name_filter = request.args.get("room_name", "")
    surname_filter = request.args.get("surname", "")
    available_seats_filter = request.args.get("available_seats") if "available_seats" in request.args else ""

    # Creazione del filtro regex per il nome
    name_regex = {"name": {"$regex": room_name_filter, "$options": "i"}}

    # Creazione del filtro regex per il cognome del minore
    guest_ids = list(db["children"].find({"surname": {"$regex": surname_filter, "$options": "i"}}).distinct("_id"))
    guest_ids = [str(guest_id) for guest_id in guest_ids]  # Conversione in stringhe
    guest_filter = {"guests": {"$in": guest_ids}}

    # Creazione del filtro per i posti liberi
    if available_seats_filter:
        available_seats_filter = int(available_seats_filter)
        if available_seats_filter >= 0:
            seats_filter = {"seats.available": available_seats_filter}
        else:
            seats_filter = {"$or": [{"seats.available": 0}, {"guests": []}]}

    # Composizione finale del filtro
    filters = {}
    if room_name_filter:
        filters.update(name_regex)
    if surname_filter:
        filters.update(guest_filter)
    if available_seats_filter != "" and available_seats_filter >= -1:
        filters.update(seats_filter)

    # Query per il conteggio totale delle stanze filtrate
    total_rooms = db["rooms"].count_documents(filters)

    if page:
        offset = (page - 1) * limit
        # Query per ottenere le stanze filtrate in ordine alfabetico con paginazione
        rooms = list(db["rooms"].find(filters).sort("name", 1).skip(offset).limit(limit))
        total_pages = math.ceil(total_rooms / limit)
    else:
        rooms = list(db["rooms"].find(filters).sort("name", 1))

    for room in rooms:
        guest_ids = room.get("guests", [])
        guest_ids = [ObjectId(guest_id) for guest_id in guest_ids]
        children = list(db["children"].find({"_id": {"$in": guest_ids}}))
        room["guests"] = children
    if page:
        response = {
            "page": page,
            "limit": limit,
            "total_rooms": total_rooms,
            "total_pages": total_pages,
            "rooms": rooms,
        }
    else:
        response = {"total_rooms": total_rooms, "rooms": rooms}

    return jsonify(response)


def rooms_room_id_patch(id):
    try:
        db = get_mongo().cx.get_default_database()
        body = request.json
        room = db["rooms"].find_one({"_id": ObjectId(id)})
        if not room:
            return jsonify({"success": False, "message": "Room not found."}), 404
        guest_ids = body.get("guests", [])
        guest_ids = [ObjectId(guest_id) for guest_id in guest_ids]
        if len(guest_ids) > room["seats"]["total"]:
            return jsonify({"success": False, "message": "number of guests greater than total seats"}), 409
        children_count = db["children"].count_documents({"_id": {"$in": guest_ids}})
        if children_count != len(guest_ids):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "One of more of the guests id are not present in children collection.",
                    }
                ),
                404,
            )
        if len(guest_ids) >= 0:
            occupied_seats = len(guest_ids)
        else:
            occupied_seats = room["seats"]["occupied"]
        body["seats"]["occupied"] = occupied_seats
        available_seats = body["seats"]["total"] - occupied_seats
        if available_seats < 0:
            return jsonify({"success": False, "message": "Error available_seats must be greater equal 0."}), 400
        body["seats"]["available"] = available_seats

        db["rooms"].update_one({"_id": ObjectId(id)}, {"$set": body})
        return jsonify({"success": True, "message": "Room successfully updated."}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def rooms_room_id_delete(id):
    try:
        db = get_mongo().cx.get_default_database()
        result = db["rooms"].delete_one({"_id": ObjectId(id)})

        if result.deleted_count > 0:
            return jsonify({"success": True, "message": "Room successfully deleted."})
        else:
            return jsonify({"success": False, "message": "Room not found."}), 404

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def rooms_room_id_get(id):
    db = get_mongo().cx.get_default_database()
    room = db["rooms"].find_one({"_id": ObjectId(id)})

    if room:
        guest_ids = room.get("guests", [])
        guest_ids = [ObjectId(guest_id) for guest_id in guest_ids]
        children = list(db["children"].find({"_id": {"$in": guest_ids}}))

        room["guests"] = children

        return jsonify(room)
    else:
        return jsonify({"message": "Stanza non trovata."}), 404
