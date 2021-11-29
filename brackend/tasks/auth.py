import datetime

import bcrypt
import jwt
from firebase_admin.auth import generate_email_verification_link, create_user

from brackend.util import SECRET_KEY, BrackendException

EXPIRY_DAYS = 14

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

