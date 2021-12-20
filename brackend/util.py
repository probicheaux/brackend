import yagmail
from pathlib import Path
import os
from dotenv import load_dotenv
ROOT_PATH = Path(__file__).parent.parent
load_dotenv(str(ROOT_PATH / ".env"))
SECRET_KEY = os.environ["SECRET_KEY"]
YAGMAIL_CLIENT = yagmail.SMTP("smusbracket@gmail.com", oauth2_file=str(ROOT_PATH / "gmail-auth.json"))
DOCKER_POSTGRES_URL = "postgresql://postgres:postgres@db/brackend"

def send_email(address, subject, message):
    YAGMAIL_CLIENT.send(to=address, subject=subject, contents=message)

class BrackendException(Exception):
    pass
