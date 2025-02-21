from bson import ObjectId


def get_resource(db, module, type):
    m = None
    t = None
    task_settings = db["settings"].find_one(
        {"type": "task", "settings.hccpModules._id": ObjectId(module)},
        {"settings.hccpModules.$": 1},
    )
    if task_settings:
        m = task_settings["settings"]["hccpModules"][0]["label"]
        for mod in task_settings["settings"]["hccpModules"][0]["modules"]:
            if mod["_id"] == ObjectId(type):
                t = mod["label"]
    return m, t


def get_element(db, type, setting_type, id):
    element = db["settings"].aggregate(
        [
            {"$match": {"type": type, f"settings.{setting_type}._id": id}},
            {"$unwind": "$settings"},
            {"$unwind": f"$settings.{setting_type}"},
            {"$match": {"type": type, f"settings.{setting_type}._id": id}},
            {"$project": {f"settings.{setting_type}": 1}},
        ]
    )
    element = list(element)
    return element[0]["settings"][setting_type]
