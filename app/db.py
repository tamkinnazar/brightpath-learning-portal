from google.cloud.sql.connector import Connector
import os

def get_db_connection():
    # Back to your clean, original setup
    connector = Connector()
    
    conn = connector.connect(
        os.getenv("DB_CONNECTION_NAME"),
        "pymysql",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME")
    )
    return conn