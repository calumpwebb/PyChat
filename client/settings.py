import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

load_dotenv(verbose=True)

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Configuration(object):
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
    )

    API_URL = os.environ.get("API_URL")
    ENV = os.environ.get("ENV", "PROD")

    # allows us to skip log in when in dev mode
    SKIP_LOGIN = os.environ.get("SKIP_LOGIN", "false").lower() == "true"
    DEV_USERNAME = os.environ.get("DEV_USERNAME")
    DEV_PASSWORD = os.environ.get("DEV_PASSWORD")

