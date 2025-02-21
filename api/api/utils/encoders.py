import base64
import datetime

from bson import ObjectId
from flask.json import JSONEncoder as _JSONEncoder


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        if isinstance(o, ObjectId):
            return o.__str__()
        if isinstance(o, bytes):
            return base64.b64encode(o).decode("UTF-8")

        return super(JSONEncoder, self).default(o)

    def dumps(self, app=None, **kwargs):
        return _JSONEncoder.dumps(self, app=app, **kwargs)
