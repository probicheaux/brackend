import logging
import os

from dotenv import load_dotenv

from brackend.app import app

gunicorn_logger = logging.getLogger("gunicorn.info")

load_dotenv(".env")
SECRET_KEY = os.environ["SECRET_KEY"]
