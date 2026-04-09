from flask import Flask
import redis

app = Flask(__name__)

# Connect to Redis using the SERVICE NAME 'redis' as the hostname.
# Docker Compose automatically creates DNS entries for each service,
# so 'redis' resolves to the Redis container's IP address.
r = redis.Redis(host='redis', port=6379)


@app.route('/')
def counter():
    # Atomically increment the 'visits' key in Redis
    count = r.incr('visits')
    return f'''
        <h1>🐳 Flask + Redis Demo</h1>
        <p>This page has been visited <strong>{count}</strong> time(s).</p>
        <p>Refresh the page to increment the counter!</p>
        <p><small>Counter is stored in Redis and persists as long as the container is running.</small></p>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
