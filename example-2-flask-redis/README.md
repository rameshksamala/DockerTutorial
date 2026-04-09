# Example 2 – Flask + Redis (Visit Counter)

Two services working together: Flask stores a visit counter in Redis.

## How to Run

```bash
docker compose up --build
```

Then open: **http://localhost:5000** — and refresh the page to see the counter go up!

## How to Stop

```bash
docker compose down
```

## Key Learning: Service-to-Service Communication

In `app.py`, Flask connects to Redis like this:

```python
r = redis.Redis(host='redis', port=6379)
```

The hostname `redis` is the **service name** from `docker-compose.yml`.  
Docker Compose automatically sets up DNS so that service names resolve to each container's internal IP.

You do **not** need to know IP addresses — just use the service name!

## Project Structure

```
example-2-flask-redis/
├── app.py              # Flask app with Redis counter
├── requirements.txt    # Python dependencies
├── Dockerfile          # Instructions to build the web image
└── docker-compose.yml  # Two services: web + redis
```
