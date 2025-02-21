import werkzeug


class ApiException(werkzeug.exceptions.HTTPException):
    pass


class InvalidSchemaException(ApiException):
    code = 400
    description = "given data are invalid"
    name = "invalid_schema"


class InvalidIdException(ApiException):
    code = 400
    description = "given id is invalid"
    name = "invalid_id"


class SubscriberNotFound(ApiException):
    code = 404
    description = "Subscriber not found"
    name = "subscriber_not_found"


class UserNotFound(ApiException):
    code = 404
    description = "User not found"
    name = "user_not_found"


class UserIsNotAuthorized(ApiException):
    code = 403
    name = "user_is_not_authorized"

    def __init__(self, authorizations, match_all: bool = True):
        """
        :param authorizations: list of failed authz
        :param match_all: bool, if False, current_user is authorized if at least one authz match,
        else the user must have all the *authorizations authz
        :return:
        """
        if match_all:
            self.description = f"You need '{authorizations}' authorization(s) to perform this action"
        else:
            self.description = f"You need at least one of '{authorizations}' authorization to perform this action"


class InvalidUsage(ApiException):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


class ForbiddenException(ApiException):
    pass
