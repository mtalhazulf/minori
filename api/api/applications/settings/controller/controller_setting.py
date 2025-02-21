from datetime import datetime

from bson import ObjectId
from flask import jsonify

from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo
from api.utils.session import get_current_user


def settings_setting_user_get(arg):
    db = get_mongo().cx.get_default_database()
    user_settings = db["settings"].find_one({"type": "user"})
    if arg in user_settings["settings"]:
        return jsonify(user_settings["settings"][arg])
    return jsonify_mongo([])


def settings_setting_task_get():
    db = get_mongo().cx.get_default_database()
    task_settings = db["settings"].find_one({"type": "task"})
    if "hccpModules" in task_settings["settings"]:
        return jsonify(task_settings["settings"]["hccpModules"])
    return jsonify([])


def settings_setting_task_cid_post(cid, body):
    db = get_mongo().cx.get_default_database()
    task_settings = db["settings"].find_one({"type": "task"})

    # category_name = body["category_name"]  # Categoria di task a cui aggiungere il modulo
    label = body["label"]  # Etichetta del modulo da creare
    name = body["name"]  # Nome del modulo da creare
    description = body["description"]  # Nome del modulo da creare

    if "hccpModules" in task_settings["settings"]:
        # Trova la categoria di task corrispondente
        categories = task_settings["settings"]["hccpModules"]
        category = next((c for c in categories if c["_id"] == ObjectId(cid)), None)
        # category = next((c for c in task_settings["settings"]["hccpModules"] if c["name"] == category_name), None)
        if category:
            # Crea il nuovo modulo
            new_module = {"_id": ObjectId(), "description": description, "label": label, "name": name}

            # Aggiungi il nuovo modulo alla lista dei moduli della categoria
            category["modules"].append(new_module)

            # Aggiorna il documento nel database
            db["settings"].update_one({"type": "task"}, {"$set": task_settings})

            return jsonify({"message": "Modulo creato con successo!"})
        else:
            return jsonify({"message": "Categoria di task non trovata."}), 404
    else:
        return jsonify({"message": "Nessuna categoria di task presente."}), 404


def settings_setting_task_post(body):
    db = get_mongo().cx.get_default_database()
    task_settings = db["settings"].find_one({"type": "task"})
    hccp_modules = task_settings["settings"]["hccpModules"]

    label = body["label"]  # Etichetta del modulo da creare
    name = body["name"]  # Nome del modulo da creare
    description = body["description"]  # Nome del modulo da creare

    new_category = {"_id": ObjectId(), "description": description, "label": label, "name": name, "modules": []}

    hccp_modules.append(new_category)

    db["settings"].update_one({"_id": task_settings["_id"]}, {"$set": {"settings.hccpModules": hccp_modules}})
    return jsonify({"message": "Categoria creata con successo!"})


def settings_setting_task_cid_mid_delete(cid, mid):
    db = get_mongo().cx.get_default_database()
    task_settings = db["settings"].find_one({"type": "task"})

    if "hccpModules" in task_settings["settings"]:
        categories = task_settings["settings"]["hccpModules"]
        category = next((c for c in categories if c["_id"] == ObjectId(cid)), None)

        if category:
            modules = category["modules"]
            module = next((m for m in modules if (m["_id"]) == ObjectId(mid)), None)

            if module:
                # Rimuovi il modulo dalla lista dei moduli della categoria
                modules.remove(module)

                # Aggiorna il documento nel database
                db["settings"].update_one({"type": "task"}, {"$set": task_settings})

                return jsonify({"message": "Modulo eliminato con successo!"})
            else:
                return jsonify({"message": "Modulo non trovato nella categoria."}), 404
        else:
            return jsonify({"message": "Categoria di task non trovata."}), 404
    else:
        return jsonify({"message": "Nessuna categoria di task presente."}), 404


def settings_setting_task_cid_mid_patch(body, cid, mid):
    db = get_mongo().cx.get_default_database()
    task_settings = db["settings"].find_one({"type": "task"})

    if "hccpModules" in task_settings["settings"]:
        categories = task_settings["settings"]["hccpModules"]
        category = next((c for c in categories if c["_id"] == ObjectId(cid)), None)

        if category:
            modules = category["modules"]
            module = next((m for m in modules if (m["_id"]) == ObjectId(mid)), None)

            if module:
                # Aggiorna i valori desiderati nel documento del modulo
                module["label"] = body.get("label", module["label"])
                module["name"] = body.get("name", module["name"])
                module["description"] = body.get("description", module["description"])

                # Aggiorna il documento delle impostazioni con l'array aggiornato hccpModules
                db["settings"].update_one({"type": "task"}, {"$set": task_settings})

                return jsonify({"message": "Modulo modificato con successo!"})
            else:
                return jsonify({"message": "Modulo non trovato nella categoria."}), 404
        else:
            return jsonify({"message": "Categoria di task non trovata."}), 404
    else:
        return jsonify({"message": "Nessuna categoria di task presente."}), 404


def settings_setting_task_cid_delete(cid):
    db = get_mongo().cx.get_default_database()
    task_settings = db["settings"].find_one({"type": "task"})

    categories = task_settings["settings"]["hccpModules"]
    category = next((c for c in categories if c["_id"] == ObjectId(cid)), None)

    if category:
        # Rimuovi la categoria e tutti i moduli associati
        categories.remove(category)

        # Aggiorna il documento nel database
        db["settings"].update_one({"_id": task_settings["_id"]}, {"$set": {"settings.hccpModules": categories}})

        return jsonify({"message": "Categoria eliminata con successo!"})
    else:
        return jsonify({"message": "Categoria non trovata."}), 404


def settings_setting_task_cid_patch(body, cid):
    db = get_mongo().cx.get_default_database()

    task_settings = db["settings"].find_one({"type": "task"})
    hccp_modules = task_settings["settings"]["hccpModules"]

    # Trova la categoria corrispondente all'ID specificato
    category = next((item for item in hccp_modules if str(item["_id"]) == cid), None)

    if category:
        # Aggiorna i valori desiderati nel documento della categoria
        category["label"] = body.get("label", category["label"])
        category["name"] = body.get("name", category["name"])
        category["description"] = body.get("description", category["description"])

        # Aggiorna il documento delle impostazioni con l'array aggiornato hccpModules
        db["settings"].update_one({"_id": task_settings["_id"]}, {"$set": {"settings.hccpModules": hccp_modules}})

        return jsonify({"message": "Categoria aggiornata con successo!"})
    else:
        return jsonify({"message": "Categoria non trovata."}), 404


def settings_setting_user_roles_post(body):
    db = get_mongo().cx.get_default_database()
    user_settings = db["settings"].find_one({"type": "user", "settings.roles.name": body["name"]})
    if not user_settings:
        _id = ObjectId()
        today = datetime.now()
        body["creation_date"] = today
        body["creationUser"] = ObjectId(get_current_user().uid)
        body["average_hour_cost"] = round(float(body["average_hour_cost"]), 2)
        body["_id"] = _id
        updated = db["settings"].update_one(
            {"type": "user"},
            {
                "$push": {
                    "settings.roles": body,
                }
            },
        )
        if updated.matched_count > 0:
            return jsonify(success=True)
        else:
            return jsonify(success=False)
    else:
        return jsonify(success=False, msg="Il livello esiste già")


def settings_setting_user_role_arg_put(arg, body):
    db = get_mongo().cx.get_default_database()
    body["_id"] = ObjectId(arg)
    updated = db["settings"].update_one(
        {"type": "user", "settings.roles._id": ObjectId(arg)},
        {"$set": {"settings.roles.$": body}},
    )
    if updated.matched_count > 0:
        return jsonify(success=True)
    else:
        return jsonify(success=False)


def settings_setting_user_role_arg_delete(arg):
    db = get_mongo().cx.get_default_database()
    updated = db["settings"].update_one({"type": "user"}, {"$pull": {"settings.roles": {"_id": ObjectId(arg)}}})
    if updated.matched_count > 0:
        return jsonify(success=True)
    else:
        return jsonify(success=False)


def settings_setting_iva_post(body):
    db = get_mongo().cx.get_default_database()
    value = body.get("value")
    timestamp = body.get("timestamp")
    iva = db["settings"].find_one({"type": "iva"})
    if not iva:
        iva_id = (
            db["settings"]
            .insert_one({"type": "iva", "value": value, "history": [{"value": value, "timestamp": timestamp}]})
            .inserted_id
        )
        if iva_id is None:
            return jsonify(success=False)
        else:
            return jsonify(success=True)
    else:
        result = db["settings"].update_one(
            {"type": "iva"}, {"$set": {"value": value}, "$push": {"history": {"value": value, "timestamp": timestamp}}}
        )
        if result.matched_count > 0:
            return jsonify({"success": True, "message": "Iva successfully added."}), 200
        else:
            return jsonify({"success": False, "message": "Problem finding IVA."}), 404


def settings_setting_iva_get():
    db = get_mongo().cx.get_default_database()
    iva = db["settings"].find_one({"type": "iva"})
    if iva:
        return jsonify(iva)
    else:
        return jsonify({"success": False, "message": "IVA not found."}), 404
