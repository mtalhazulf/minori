from datetime import datetime

from bson import ObjectId

from api.middleware.mongo import get_mongo
from api.utils.session import get_current_user


class Log:
    application = None  # type of application logged (document,asset,ticketing etc)
    timestamp = None  # timestamp of the log
    subject = None  # subject of the log related to the application
    action = None  # action logged related to the subject
    resource = None  # resource related if needed (ObjectId)
    user = None  # current user

    def __init__(self, application, subject, action, resource=None):
        self.application = application
        self.timestamp = datetime.now()
        self.action = action
        self.subject = subject
        self.user = ObjectId(get_current_user().uid)

        if resource is not None:
            self.resource = resource

    def store_log(self):
        data = {
            "application": self.application,
            "timestamp": self.timestamp,
            "subject": self.subject,
            "action": self.action,
            "resource": self.resource,
            "user": self.user,
        }

        db = get_mongo().cx.get_default_database()

        return db["logs"].insert_one(data).inserted_id
