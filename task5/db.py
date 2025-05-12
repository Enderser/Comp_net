import psycopg2
from psycopg2 import OperationalError

def init_db():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except OperationalError as e:
        print(f"Error initializing database: {e}")

def get_db():
    return psycopg2.connect(
        dbname="mydb",
        user="admin",
        password="password",
        host="db",
        port="5432"
    )

def add_url(url):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO urls (url) VALUES (%s)", (url,))
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_urls():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, url FROM urls")
    urls = [{"id": row[0], "url": row[1]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return urls