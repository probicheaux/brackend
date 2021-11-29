import logging
import os
from pathlib import Path

import firebase_admin

from brackend.app import app
from brackend.util import ROOT_PATH

gunicorn_logger = logging.getLogger("gunicorn.info")


def init_firebase():
    firebase_credentials_path = str(ROOT_PATH / "firebase-credentials.json")
    credentials = firebase_admin.credentials.Certificate(firebase_credentials_path)
    default_app = firebase_admin.initialize_app(credentials)
    return default_app


init_firebase()
