import datetime
from flask import request
from functools import wraps

import bcrypt
import jwt
from firebase_admin.auth import create_user, generate_email_verification_link, verify_id_token
from flask_restful import abort

from brackend.util import SECRET_KEY, BrackendException

EXPIRY_DAYS = 14


def abrt():
    abort(401, message="Authorization Required")


def auth_decorator(meth):
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
        return meth(firebase_id, *args, **kwargs)

    return wrapper


class AuthenticationError(BrackendException):
    pass


def encode_auth_token(user_id):
    """Generates the Auth Token."""
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=EXPIRY_DAYS),
        "iat": datetime.datetime.utcnow(),
        "sub": user_id,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def get_password_and_salt(password):
    salt = bcrypt.gensalt()
    password = password.encode()
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode()


def check_password(hashed, password):
    hashed = hashed.encode()
    password = password.encode()
    return bcrypt.checkpw(password, hashed)


def generate_verification_email(email_address):
    link = generate_email_verification_link(email_address)
    body = f"Click the link to verify your smus bracket account :)\n\n{link}"
    return body


def create_user_firebase(email_address):
    return create_user(email=email_address)
