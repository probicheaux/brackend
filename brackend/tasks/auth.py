import datetime

import jwt
from brackend import SECRET_KEY

EXPIRY_DAYS = 14


def encode_auth_token(user_id):
    """Generates the Auth Token."""
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=EXPIRY_DAYS),
        "iat": datetime.datetime.utcnow(),
        "sub": user_id,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
