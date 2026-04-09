from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello from Docker Compose! 🐳</h1><p>Your Flask app is running inside a container.</p>'


if __name__ == '__main__':
    # IMPORTANT: host='0.0.0.0' makes Flask listen on all interfaces
    # inside the container, so it's reachable from your browser.
    app.run(host='0.0.0.0', port=5000, debug=True)
