import os
import uuid
from pathlib import Path

import yagmail
from dotenv import load_dotenv

ROOT_PATH = Path(__file__).parent.parent
load_dotenv(str(ROOT_PATH / ".env"))
SECRET_KEY = os.environ["SECRET_KEY"]
YAGMAIL_CLIENT = yagmail.SMTP(
    "smusbracket@gmail.com", oauth2_file=str(ROOT_PATH / "gmail-auth.json")
)
AUTHENTICATING = os.environ["DEV"] == 1


def send_email(address, subject, message):
    YAGMAIL_CLIENT.send(to=address, subject=subject, contents=message)


class BrackendException(Exception):
    pass


def random_string():
    """Returns a random string of length 10."""
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-", "")
    return random[:10]
