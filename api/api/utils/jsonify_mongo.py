from bson import json_util
from flask import Response


def jsonify_mongo(obj):
    return Response(json_util.dumps(obj), mimetype="application/json")
