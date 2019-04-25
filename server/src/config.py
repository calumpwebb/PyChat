import datetime
import os
import platform
import re

from sqlalchemy import create_engine, engine, event
from sqlalchemy.orm import Session, scoped_session, sessionmaker

_SESSION = None


class Configuration(object):
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
    )

    DB_URI = os.environ.get(
        "DB_RUI", "postgresql://postgres:password@localhost:5433/pychat"
    )

    SECRET_KEY = os.environ.get("SECRET_KEY", "this_is_the_secret_key")

    # DECIDES WHETHER TO RUN THE WEBSOCKET OR API SERVER
    SERVER_TYPE = os.environ.get("SERVER_TYPE")

    # CAPTURES SQL QUERIES AND PRINTS THEM BEFORE THEY EXECUTE
    PRINT_SQL_QUERIES = os.environ.get("PRINT_SQL_QUERIES", "false").lower() == "true"


def get_session(uri=None) -> Session:
    """
    Returns a fully configured SQLAlchemy session.
    """
    global _SESSION

    if _SESSION:
        return _SESSION()

    database_uri = uri or Configuration.DB_URI

    engine = create_engine(
        database_uri,
        connect_args={
            "application_name": "{}-{}".format(platform.node(), os.getpid()),
            "connect_timeout": 60 * 60 * 3,
        },
        pool_recycle=60 * 60,
        pool_pre_ping=True,
        implicit_returning=True,
    )

    session_factory = sessionmaker(bind=engine)
    _SESSION = scoped_session(session_factory)
    return _SESSION()


@event.listens_for(engine.Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, exceutemany):
    if Configuration.PRINT_SQL_QUERIES:
        if isinstance(parameters, dict):
            conn.info["query_start"] = datetime.datetime.now()
            actual_query = cursor.mogrify(statement, parameters)
            query = actual_query.decode("utf-8").replace("\\n", "\n")

            print(query)
        else:
            print("not formatting parameters is not a dict")


@event.listens_for(engine.Engine, "after_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, exceutemany):
    if Configuration.PRINT_SQL_QUERIES:
        start_time = conn.info.get("query_start")
        if start_time:
            print("query time", datetime.datetime.now() - start_time, "\n")
