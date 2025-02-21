from bson import ObjectId
from flask import Response, jsonify
from werkzeug.exceptions import BadRequest, UnprocessableEntity

from api.applications.auth.helper.attendance import (
    add_attendance,
    can_login,
    can_manual_login,
)
from api.applications.tasks.helper.notebook import get_summary
from api.middleware.mongo import get_mongo
from api.utils.db_user import DBUser
from api.utils.log import Log
from api.utils.session import CookieSession, Session, get_current_user


def auth_login_manual_post(body):
    body["usertype"] = "user"
    start_date = body.pop("start_date", None)
    if start_date:
        data = {"start_date": start_date}
    else:
        data = None
    user_instance = DBUser.initialize(**body, check_enabled=True, check_activation_key=True)

    response = Response(
        response=user_instance.json_serialize(),
        status=200,
        mimetype="application/json",
    )
    if user_instance.badgeId is None:
        raise BadRequest("Impossibile effettuare l'accesso.L'utente non possiede un badge associato.")
    if (
        user_instance.status == "enabled"
        and user_instance.usertype != "admin"
        and user_instance.usertype != "superadmin"
    ):
        login = can_manual_login(body["subscriber"], start_date, response.json["uid"])
        if login[0]:
            session = CookieSession(db_user=user_instance)
            session.set_context()
            session.set_cookie_session(response)
            Log(application="auth", subject="user", action="login").store_log()
            attendance_response = response
            resp = jsonify(success=add_attendance(response, data))
            if resp:
                attendance_response = jsonify(
                    {
                        "status": "pending",
                        "msg": "La richiesta è stata effettuata! "
                        "L'amministatore deciderà se accettarla o meno,"
                        " riprova ad accedere più tardi!",
                    }
                )
            return attendance_response
        else:
            raise BadRequest(login[1])
    else:
        raise BadRequest(
            (
                "L'operatore è stato disabilitato"
                if user_instance.status != "enabled"
                else "L'amministratore non ha bisogno di effettuare la timbratura. Effettua il login."
            )
        )


def auth_login(body):
    body["usertype"] = "user"
    user_instance = DBUser.initialize(**body, check_enabled=True, check_activation_key=True)

    response = Response(response=user_instance.json_serialize(), status=200, mimetype="application/json")
    if user_instance.status == "enabled":
        login = can_login(body["subscriber"], response.json["uid"])
        if login[0] or response.json["usertype"] == "admin" or response.json["usertype"] == "superadmin":
            session = CookieSession(db_user=user_instance)
            session.set_context()
            session.set_cookie_session(response)
            Log(application="auth", subject="user", action="login").store_log()
            return response
        else:
            raise BadRequest(login[1])
    else:
        raise BadRequest("L'operatore è stato disabilitato")


def auth_logout_post(body):
    Log(application="auth", subject="user", action="logout").store_log()
    session = Session.get_context()
    session = CookieSession(session)
    if isinstance(session, CookieSession):
        """db = get_mongo().cx.get_default_database()
        db["attendance"].update_one(
            {"userId": ObjectId(body["user"]), "status": "enabled", "end_date": None},
            {"$set": {"end_date": datetime.now()}},
        )"""
        response = jsonify(response=True)
        session.unset_cookie_session(response)
        return response
    raise UnprocessableEntity("Impossibile effettuare il logout.")


def auth_logout_arg_get(arg):
    db = get_mongo().cx.get_default_database()
    tasks = get_summary(db, arg)
    if tasks["total"] > 0 and tasks["total"] != tasks["done"]:
        active_operators = list(
            db["attendance"].find(
                {
                    "status": "enabled",
                    "end_date": None,
                    "userId": {"$ne": ObjectId(get_current_user().uid)},
                }
            )
        )
        if len(active_operators) == 0:
            return jsonify({"success": False})
    return jsonify({"success": True})


def auth_token_access(body):
    user_instance = DBUser.initialize(**body, check_enabled=True, check_activation_key=True)

    session = Session(user_instance, "bearer")
    session.set_context()

    Log(application="auth", subject="access-token", action="generated").store_log()

    return jsonify({"token": session.serialize()})


def auth_token_refresh():
    session = Session.get_context()
    if isinstance(session, CookieSession) or session.auth_method != "bearer":
        raise UnprocessableEntity()

    Log(application="auth", subject="access-token", action="refreshed").store_log()
    return jsonify({"token": session.serialize()})
