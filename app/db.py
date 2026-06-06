from google.cloud.sql.connector import Connector
import os
from contextlib import contextmanager

# 1. Initialize a single static connector instance. 
# This prevents Gunicorn from spinning up infinite background authentication loops.
_connector = None

def _get_connector():
    global _connector
    if _connector is None:
        _connector = Connector()
    return _connector

# 2. A clean context manager that handles opening and auto-closing your DB links
@contextmanager
def get_db_connection():
    conn = None
    try:
        connector = _get_connector()
        conn = connector.connect(
            os.getenv("DB_CONNECTION_NAME"),
            "pymysql",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME")
        )
        yield conn
    finally:
        if conn:
            conn.close()