import os
from google.cloud.sql.connector import Connector
import pymysql

connector = Connector()

def get_db_connection():
    conn = connector.connect(
        os.getenv("DB_CONNECTION_NAME"),
        "pymysql",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME")
    )
    return conn