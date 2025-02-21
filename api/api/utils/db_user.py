from datetime import datetime
from hashlib import sha512

from bson import ObjectId
from flask import current_app
from werkzeug.exceptions import InternalServerError, Unauthorized

from api.exceptions import SubscriberNotFound, UserNotFound
from api.middleware.mongo import get_mongo


class DBUser:
    id = None
    uid = None
    username = None
    usertype = None
    subscriber = None
    subscriber_id = None
    authorizations = None
    groups = None
    session_time = None

    def __init__(
        self,
        uid,
        username,
        subscriber,
        subscriber_id,
        usertype,
        authorizations=None,
        groups=None,
        id=None,
        session_time=None,
        **kwargs
    ):
        if id is None:
            self.id = subscriber + "-" + uid
        else:
            self.id = id
        self.uid = uid
        self.username = username
        self.usertype = usertype
        self.subscriber = subscriber
        self.authorizations = authorizations if isinstance(authorizations, list) else []
        self.groups = groups if isinstance(groups, list) else []
        self.subscriber_id = subscriber_id
        self.session_time = session_time
        self.url = kwargs.get("url") if "url" in kwargs else None
        self.accounting_url = kwargs.get("accounting_url") if "accounting_url" in kwargs else None
        self.badgeId = kwargs.get("badgeId") if "badgeId" in kwargs else None
        self.name = kwargs.get("name")
        self.surname = kwargs.get("surname")
        self.company_name = kwargs.get("companyName")
        self.status = "enabled" if kwargs.get("status") is None else kwargs.get("status")

    @property
    def is_active(self):
        return self.is_authenticated

    @property
    def is_authenticated(self):
        return self.id is not None

    @property
    def is_anonymous(self):
        return not self.is_authenticated

    @staticmethod
    def hash_password(password):
        return sha512(password.encode("ascii")).hexdigest()

    @classmethod
    def initialize(
        cls,
        subscriber: str,
        id: ObjectId = None,
        username: str = None,
        usertype: str = "subuser",
        password=None,
        check_enabled=False,
        check_activation_key=False,
    ):
        mongo = get_mongo()

        subscriber_user = mongo.cx.get_default_database()["users"].find_one({"username": subscriber})
        if subscriber_user is None:
            raise SubscriberNotFound()

        if usertype == "admin" or usertype == "superadmin":
            db = mongo.cx.get_default_database()
            user = subscriber_user
        else:
            db = mongo.cx.get_default_database()
            if id is not None:
                user = db.users.find_one({"_id": id})
            elif username is not None:
                user = db.users.find_one({"username": username.lower()})
            else:
                raise InternalServerError("No username or ObjectId given")
            if user is None:
                raise UserNotFound()

        if password is not None:
            password = cls.hash_password(password)
            if password != user["password"]:
                raise Unauthorized("invalid_credentials")

        if "subscriber" not in user:
            user["subscriber"] = subscriber

        if "type" in user:
            usertype = user["type"]

        return cls(
            uid=user["_id"].__str__(),
            subscriber_id=subscriber_user["_id"].__str__(),
            usertype=usertype,
            session_time=datetime.now(),
            **user
        )

    def get_subscriber(self, full_account=False):
        if not full_account:
            return self.subscriber
        return get_mongo().cx.get_default_database()["users"].find_one({"username": self.subscriber})

    def get_subscriber_id(self, object_id=True):
        if object_id:
            return ObjectId(self.subscriber_id)
        return self.subscriber_id

    def get_userid(self, object_id=True):
        if object_id:
            return ObjectId(self.uid)
        return self.uid

    def get_groups(self, object_id=True):
        if object_id:
            return [ObjectId(x) for x in self.groups]
        return self.groups

    def get_db(self):
        return get_mongo().cx.get_default_database()

    def get_workspace(self, application: str = None, key: str = None):
        ws = self.get_db()["users"].find_one({"_id": self.get_userid(object_id=True)}, {"workspace": 1})
        if "workspace" not in ws:
            return {}

        if application is None:
            return ws["workspace"]

        if application not in ws["workspace"]:
            return {}

        if key is None:
            return ws["workspace"][application]

        if key not in ws["workspace"][application]:
            return {}

        return ws["workspace"][application][key]

    def set_workspace(self, application: str, key: str, value):
        self.get_db()["users"].update_one(
            {"_id": self.get_userid(object_id=True)},
            {"$set": {"workspace." + application + "." + key: value}},
        )

    def unset_workspace(self, application: str, key: str):
        self.get_db()["users"].update_one(
            {"_id": self.get_userid(object_id=True)},
            {"$unset": {"workspace." + application + "." + key: 1}},
        )

    def is_authorized(self, authorization, expires: datetime = None, wildcard=False):
        if expires is None:
            expires = datetime.now()

        for authz in self.authorizations:
            if "expires" in authz and expires > authz["expires"]:
                continue
            if wildcard and ("wildcard" not in authz or authz["wildcard"] is False):
                continue
            if authorization == authz["authorization"]:
                return True
            if "wildcard" in authz and authz["wildcard"]:
                if len(authorization) < len(authz["authorization"]):
                    continue

                # special empty wildcard authz
                if len(authz["authorization"]) == 0:
                    return True

                if (
                    authorization[0 : len(authz["authorization"])] == authz["authorization"]
                    and authorization[len(authz["authorization"])] == "."
                ):
                    return True
        return False

    def serialize(self):
        authorizations = []
        for authz in self.authorizations:
            if "expires" in authz and isinstance(authz["expires"], datetime):
                authz["expires"] = authz["expires"].isoformat()
            authorizations += [authz]

        serialized = {
            "id": self.id,
            "uid": self.uid,
            "username": self.username,
            "usertype": self.usertype,
            "subscriber": self.subscriber,
            "subscriber_id": self.subscriber_id,
            "authorizations": self.authorizations,
            "groups": self.groups,
            "url": self.url,
            "accounting_url": self.accounting_url,
        }

        if self.name:
            serialized["name"] = self.name
        if self.surname:
            serialized["surname"] = self.surname
        if self.company_name:
            serialized["companyName"] = self.company_name

        return serialized

    def json_serialize(self):
        return current_app.json_encoder().encode(self.serialize())

    @classmethod
    def unserialize(cls, d):
        _authorizations = d["authorizations"] if "authorizations" in d else []
        authorizations = []
        for authorization in _authorizations:
            if "expires" in authorization and isinstance(authorization["expires"], str):
                authorization["expires"] = datetime.fromisoformat(authorization["expires"])
            authorizations += [authorization]

        d["authorizations"] = authorizations
        return cls(**d)
