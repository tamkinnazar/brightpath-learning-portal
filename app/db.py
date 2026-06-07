import pymysql
import os

def get_db_connection():
    # Back to the fully private, internal VPC network path
    conn = pymysql.connect(
        host="10.220.0.3", 
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        # FIX: Try to get the env var. If it's missing, fall back to your actual database schema name string
        database=os.getenv("DB_NAME", "appdb"), 
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10
    )
    return conn