from functools import wraps
from flask import make_response


def allow_cross_domain(fun):
    @wraps(fun)
    def _fun(*args, **kwargs):
        resp = make_response(fun(*args, **kwargs))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        resp.headers['Access-Control-Allow-Credentials'] = True
        allow_headers = "Origin, X-Requested-With, Content-Type, Accept"
        resp.headers['Access-Control-Allow-Headers'] = allow_headers
        return resp
    return _fun

