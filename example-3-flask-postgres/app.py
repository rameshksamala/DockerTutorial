from flask import Flask
import psycopg2
import os
import time

app = Flask(__name__)


def get_db_connection():
    """Create and return a PostgreSQL connection using environment variables."""
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )


def wait_for_db(retries=10, delay=2):
    """Wait for the database to be ready (it takes a few seconds to initialize)."""
    for i in range(retries):
        try:
            conn = get_db_connection()
            conn.close()
            print("✅ Database is ready!")
            return True
        except Exception as e:
            print(f"⏳ Waiting for database... ({i+1}/{retries}): {e}")
            time.sleep(delay)
    return False


@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return f'''
            <h1>🐳 Flask + PostgreSQL Demo</h1>
            <p>✅ Successfully connected to PostgreSQL!</p>
            <p><strong>Database version:</strong> {version}</p>
            <p><small>Connection details are loaded from environment variables — no hardcoded secrets!</small></p>
        '''
    except Exception as e:
        return f'<h1>❌ Database Error</h1><p>{e}</p>', 500


@app.route('/create-table')
def create_table():
    """Create a sample messages table."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
    return '<h1>✅ Table created!</h1><a href="/add-message">Add a message</a>'


@app.route('/add-message')
def add_message():
    """Insert a sample message into the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (content) VALUES (%s) RETURNING id", ('Hello from Flask! 👋',))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return f'<h1>✅ Message inserted with ID: {new_id}</h1><a href="/messages">View all messages</a>'


@app.route('/messages')
def list_messages():
    """List all messages from the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, content, created_at FROM messages ORDER BY created_at DESC')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    rows_html = ''.join(f'<li>#{r[0]}: {r[1]} <em>({r[2]})</em></li>' for r in rows)
    return f'<h1>Messages</h1><ul>{rows_html or "<li>No messages yet.</li>"}</ul><a href="/add-message">Add more</a>'


if __name__ == '__main__':
    wait_for_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
