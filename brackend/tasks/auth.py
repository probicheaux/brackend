from functools import wraps

from firebase_admin.auth import verify_id_token
from flask import request
from flask_restful import abort


def abrt():
    """Abort with a 401 response code."""
    abort(401, message="Authorization Required")


def auth_decorator(meth):
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
