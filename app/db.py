from google.cloud.sql.connector import Connector
import os

# Initialize the connector once globally as a singleton.
# This prevents Gunicorn from exhausting background threads.
_connector = None

def get_db_connection():
    global _connector
    if _connector is None:
        _connector = Connector()
        
    conn = _connector.connect(
        os.getenv("DB_CONNECTION_NAME"),
        "pymysql",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME")
    )
    return conn