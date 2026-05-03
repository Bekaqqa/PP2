import psycopg2
from config import DB_NAME, DB_USER, DB_HOST, DB_PORT, DB_PASSWORD

def get_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT,
        password=DB_PASSWORD
    )
    return conn, conn.cursor()