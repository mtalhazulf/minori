import logging

import requests
from bson import ObjectId

from api.exceptions import ApiException


class Notification:
    VALID_NOTIFICAITON = ["email"]

    @classmethod
    def send_email(
        cls,
        sender: str,
        subscriber: str,
        title: str,
        message: str,
        users: [ObjectId] = None,
        groups: [ObjectId] = None,
        emails: [str] = None,
        all_users: bool = False,
        exceptions=False,
        template_values: dict = None,
    ):
        return cls.send(
            sender,
            subscriber,
            "email",
            title,
            message,
            users,
            groups,
            emails,
            all_users,
            exceptions,
            template_values,
        )

    @classmethod
    def send(
        cls,
        sender: str,
        subscriber: str,
        notification_system: str,
        title: str,
        message: str,
        users: [ObjectId] = None,
        groups: [ObjectId] = None,
        emails: [str] = None,
        all_users: bool = False,
        exceptions=False,
        template_values: dict = None,
    ):
        if exceptions:
            return cls._send(
                sender,
                subscriber,
                notification_system,
                title,
                message,
                users,
                groups,
                emails,
                all_users,
                template_values,
            )
        else:
            try:
                return cls._send(
                    sender,
                    subscriber,
                    notification_system,
                    title,
                    message,
                    users,
                    groups,
                    emails,
                    all_users,
                    template_values,
                )
            except BaseException as e:
                logging.error("api.utils.Notification error: " + e.__str__())

    @classmethod
    def _send(
        cls,
        sender: str,
        subscriber: str,
        notification_system: str,
        title: str,
        message: str,
        users: [ObjectId] = None,
        groups: [ObjectId] = None,
        emails: [str] = None,
        all_users: bool = False,
        template_values: dict = None,
    ):
        req_body = {
            "title": title,
            "message": message,
            "recipients": {},
            "values": template_values,
            "sender": sender,
        }

        if all_users:
            req_body["recipients"]["all"] = True
        elif users is not None and len(users) > 0:
            req_body["recipients"]["uids"] = [user.__str__() for user in users]
        if groups is not None and len(groups) > 0:
            req_body["recipients"]["gids"] = [group.__str__() for group in groups]
        if emails is not None and len(emails) > 0:
            req_body["recipients"]["emails"] = emails

        if len(req_body["recipients"]) == 0:
            raise ApiException("No users, groups or emails given", code=500)

        req_body["recipients"]["subscriber"] = subscriber
        req = requests.post("http://bach-tasks/" + notification_system, json=req_body, timeout=5)

        if req.status_code == 200:
            return req.json()
        else:
            try:
                error = req.json()
                error_name = error["error"]
            except Exception:
                raise ApiException(
                    "Error sending email, error response " + str(req.status_code),
                    description=req.content,
                    code=500,
                )
            raise ApiException(
                error_name,
                description=error["description"] if "description" in error else "",
                code=500,
            )
