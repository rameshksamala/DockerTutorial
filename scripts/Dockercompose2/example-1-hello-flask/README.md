# Example 1 – Hello World Flask

The simplest possible Docker Compose setup: one Flask service, no Dockerfile.

## How to Run

```bash
docker compose up
```

Then open your browser at: **http://localhost:5000**

You should see: *Hello from Docker Compose! 🐳*

## How to Stop

```bash
docker compose down
```

## What's Happening Here?

- `image: python:3.11-slim` — uses the official Python image from Docker Hub
- `volumes: - .:/app` — mounts your current folder into the container so it reads your `app.py`
- `ports: - '5000:5000'` — maps port 5000 on your machine to port 5000 in the container
- `command` — installs dependencies and starts the Flask app in one step

No Dockerfile needed for this simple example!
