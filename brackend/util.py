from pathlib import Path
import os
from dotenv import load_dotenv

ROOT_PATH = Path(__file__).parent.parent
load_dotenv(str(ROOT_PATH / ".env"))
SECRET_KEY = os.environ["SECRET_KEY"]
DOCKER_POSTGRES_URL = "postgresql://postgres:postgres@db/brackend"


class BrackendException(Exception):
    """
    meaningless
    """

    pass
