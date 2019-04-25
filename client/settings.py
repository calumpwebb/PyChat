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

    APP_TITLE = os.environ.get("APP_TITLE")
    APP_FOOTER = os.environ.get("APP_FOOTER")
    VERSION = os.environ.get("VERSION")