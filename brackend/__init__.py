import logging
import os
from pathlib import Path

import firebase_admin
from dotenv import load_dotenv

from brackend.app import app

gunicorn_logger = logging.getLogger("gunicorn.info")

ROOT_PATH = Path(__file__).parent
load_dotenv(ROOT_PATH / ".env")
SECRET_KEY = os.environ["SECRET_KEY"]


def init_firebase():
    firebase_credentials_path = ROOT_PATH / "firebase-credentials.json"
    credentials = firebase_admin.credentials.Certificate(firebase_credentials_path)
    default_app = firebase_admin.initialize_app(credentials)
    return default_app


init_firebase()
