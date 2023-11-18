from werkzeug.http import HTTP_STATUS_CODES
from flask import jsonify


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(code=code, message=message, **kwargs)
    response.status_code = code
    return response


def unsupported_media_type(info=None):
    res = api_abort(415, error='Unsupported Media Type', error_description=info)
    res.headers['WWW-Authenticate'] = 'Bearer'
    return res


def arg_required(info=None):
    res = api_abort(401, error='A required argument was absent', error_description=info)
    res.headers['WWW-Authenticate'] = 'Bearer'
    return res


def file_not_found(info=None):
    res = api_abort(404, error='Source not found', error_description=info)
    res.headers['WWW-Authenticate'] = 'Bearer'
    return res
