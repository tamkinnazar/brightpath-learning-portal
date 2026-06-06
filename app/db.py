import pymysql
import os

def get_db_connection():
    # Back to the fully private, internal VPC network path
    conn = pymysql.connect(
        host="10.220.0.3", 
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10
    )
    return conn