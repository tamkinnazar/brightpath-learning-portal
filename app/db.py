from google.cloud.sql.connector import Connector
import os

def get_db_connection():
    # Initialize the connector cleanly within the call block
    connector = Connector()
    
    conn = connector.connect(
        os.getenv("DB_CONNECTION_NAME"), # Maps to your GCP Instance Connection Name string
        "pymysql",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME")
    )
    return conn