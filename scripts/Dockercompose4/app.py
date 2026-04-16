import os
import time
import psycopg2
from flask import Flask

app = Flask(__name__)

# Get the connection string from the environment variable set in docker-compose.yml
DB_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    """Retries connection to the database if it's not ready yet."""
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(DB_URL)
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            print(f"Database not ready. Retrying in 2 seconds... ({retries} attempts left)")
            time.sleep(2)
    return None

@app.route('/')
def hello():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return f"<h1>Success!</h1><p>Connected to: {db_version[0]}</p>"
    else:
        return "<h1>Error</h1><p>Could not connect to the database.</p>", 500

if __name__ == "__main__":
    # Host '0.0.0.0' is required for Docker to expose the app
    app.run(host='0.0.0.0', port=5000)