from flask import make_response, redirect
from functools import wraps

import json
import traceback

class WebException(Exception): pass

response_header = { "Content-Type": "application/json; charset=utf-8" }

def api_wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        web_result = {}
        response = 200
        try:
            web_result = f(*args, **kwargs)
        except WebException as error:
            web_result = { "success": 0, "message": str(error) }
        except Exception as error:
            traceback.print_exc()
            web_result = { "success": 0, "message": "Something went wrong!", "error": [ str(error), traceback.format_exc() ] }
        result = (json.dumps(web_result), response, response_header)
        response = make_response(result)

        return response
    return wrapper

import users # Below api_wrapper to prevent import loops

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not users.is_logged_in():
            return { "success": 0, "message": "You must be logged in to do this." }
        return f(*args, **kwargs)
    return wrapper

def redirect_if_not_logged_in(route):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not users.is_logged_in():
                return redirect(route)
            return f(*args, **kwargs)
        return wrapper
    return decorator
