import pymysql
import os

def get_db_connection():
    # Connect directly via the Private VPC network using the Internal IP.
    # This keeps things lightning-fast and consumes almost zero database RAM.
    conn = pymysql.connect(
        host="10.220.0.3",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10
    )
    return conn