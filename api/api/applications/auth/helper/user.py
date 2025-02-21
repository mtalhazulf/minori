from bson import ObjectId

from api.applications.settings.helper.settings import get_element
from api.utils.log import Log


def get_active_users(db, list_users):
    return list(db["users"].find({"_id": {"$in": list_users}, "status": "enabled"}))


def get_user(db, id):
    user = db["users"].find_one({"_id": ObjectId(id)})
    if user and "role" in user:
        user["role"] = get_element(db, "user", "roles", user["role"])
    return user


def get_user_by_username(db, username):
    return db["users"].find_one(
        {
            "username": username,
            "$or": [{"status": "enabled"}, {"status": {"$exists": False}}],
        }
    )


def update_operator_badge(db, badgeId, id):
    updated = db["users"].update_one(
        {
            "_id": ObjectId(id),
        },
        {"$set": {"badgeId": badgeId}},
    )
    if updated.matched_count > 0:
        Log(
            application="auth",
            subject="user",
            action="change/assign badgeId to " + badgeId,
            resource=ObjectId(id),
        ).store_log()


def remove_operator_badge(db, id):
    updated = db["users"].update_one(
        {
            "_id": ObjectId(id),
        },
        {"$unset": {"badgeId": ""}},
    )
    if updated.matched_count > 0:
        Log(
            application="auth",
            subject="user",
            action="Removed badgeId",
            resource=ObjectId(id),
        ).store_log()
