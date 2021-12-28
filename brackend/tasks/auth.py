import logging
from functools import wraps

from firebase_admin.auth import verify_id_token
from flask import request
from flask_restful import abort, current_app

logger = logging.getLogger(__name__)


def abrt():
    """Abort with a 401 response code."""
    abort(401, message="Authorization Required")


def requires_auth_method_wrapper(meth):
    """Wraps a restful method with an auth check.

    Stuffs firebase_id into the method.
    """

    @wraps(meth)
    def wrapper(*args, **kwargs):
        bearer = request.headers.get("Authorization")
        if bearer is None:
            abrt()
        bearer, token = bearer.split(maxsplit=1)
        if bearer != "Bearer":
            abrt()

        # (TODO): Check if user is revoked here
        try:
            parsed = verify_id_token(token)
        except:
            abrt()

        firebase_id = parsed["uid"]
        # Stuffs firebase_id into the decorated method
        # Is there a better way to do this? Parse it from the token again in the method body?
        return meth(*args, **kwargs, firebase_id=firebase_id)

    return wrapper


def requires_auth(clazz):
    # Note: must use this awkward addition thing instead of mutating the method_decorators list
    # because if method decorators is defined for Resource but not Child(Resource) = clazz,
    # we'll just be mutating Resource.method_decorators
    clazz.method_decorators = clazz.method_decorators + [requires_auth_method_wrapper]
    return clazz
