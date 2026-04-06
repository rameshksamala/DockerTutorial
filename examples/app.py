"""
Simple example Python app for the Docker image guide.
This file is copied into the image in Layer 5 (COPY app.py).
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class DockerInfoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        info = {
            "message": "Hello from inside a Docker container!",
            "concept": "This app runs in the container layer (read/write) on top of read-only image layers.",
            "layers": [
                "Layer 1 — Base OS (ubuntu:22.04)",
                "Layer 2 — Python runtime (apt-get install python3)",
                "Layer 3 — requirements.txt (COPY)",
                "Layer 4 — Python packages (pip install)",
                "Layer 5 — This app (COPY app.py)",
                "Container Layer — Any runtime writes go here (read/write)",
            ],
        }
        body = json.dumps(info, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(f"[Docker Guide App] {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), DockerInfoHandler)
    print("Docker Guide app running on http://0.0.0.0:8080")
    print("Visit the endpoint to see layer info as JSON.")
    server.serve_forever()
