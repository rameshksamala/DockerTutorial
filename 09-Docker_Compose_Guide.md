# Docker Compose for Python Applications - Complete Guide

## Table of Contents
1. [Introduction](#introduction)
2. [What is Docker Compose?](#what-is-docker-compose)
3. [Key Concepts](#key-concepts)
4. [Installation](#installation)
5. [Basic Syntax](#basic-syntax)
6. [Python Project Examples](#python-project-examples)
7. [Best Practices](#best-practices)
8. [Common Commands](#common-commands)

---

## Introduction

Docker Compose is a tool for defining and running multi-container Docker applications. It uses a YAML file to configure application services, networks, and volumes. Instead of running multiple `docker run` commands, you define everything in a single `docker-compose.yml` file and start all containers with one command.

This guide provides practical examples for Python developers to quickly get started with Docker Compose.

---

## What is Docker Compose?

Docker Compose allows you to:
- **Define multiple services** in a single configuration file
- **Connect containers** through an internal network automatically
- **Share data** between containers using volumes
- **Start/stop all services** with simple commands
- **Ensure reproducible environments** across development, testing, and production

### Why Use Docker Compose?

- Simplifies container orchestration for local development
- Eliminates "works on my machine" problems
- Makes it easy to replicate production environments locally
- Speeds up the development workflow
- Improves collaboration between team members

---

## Key Concepts

### Services
Services are individual containers defined in your `docker-compose.yml`. Each service represents an application or component (e.g., web app, database, cache).

### Images
Docker images are templates used to create containers. They can be built from a Dockerfile or pulled from Docker Hub.

### Volumes
Volumes are used to persist data and share files between the host machine and containers, or between containers.

### Networks
Docker Compose automatically creates a network where all services can communicate using their service names as hostnames.

### Ports
Port mapping connects container ports to host machine ports, making services accessible outside the container.

---

## Installation

### Windows & Mac
Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)

Docker Desktop includes Docker Compose automatically.

### Linux
```bash
sudo apt-get update
sudo apt-get install docker-compose
```

Verify installation:
```bash
docker-compose --version
```

---

## Basic Syntax

### Structure of docker-compose.yml

```yaml
version: '3.8'

services:
  service_name:
    image: image_name
    container_name: container_name
    ports:
      - "host_port:container_port"
    environment:
      - ENV_VAR=value
    volumes:
      - ./local_path:/container_path
    depends_on:
      - another_service
    networks:
      - network_name

volumes:
  volume_name:

networks:
  network_name:
```

### Version
The version specifies the Compose file format. Version 3.8 is recommended for recent Docker versions.

---

## Python Project Examples

## Example 1: Simple Python Web Application with PostgreSQL

### Project Structure
```
my-python-app/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── app.py
└── .env
```

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### requirements.txt
```
Flask==2.3.0
psycopg2-binary==2.9.6
python-dotenv==1.0.0
```

### app.py
```python
from flask import Flask
import psycopg2
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'db'),
            database=os.getenv('DB_NAME', 'myapp'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres')
        )
        return conn
    except Exception as e:
        return None

@app.route('/')
def hello():
    conn = get_db_connection()
    if conn:
        return "Hello! Connected to PostgreSQL ✓"
    return "Hello! Database connection failed ✗"

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### docker-compose.yml (Example 1)
```yaml
version: '3.8'

services:
  # Python Web Application
  web:
    build: .
    container_name: python_web_app
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=app.py
      - DB_HOST=db
      - DB_NAME=myapp
      - DB_USER=postgres
      - DB_PASSWORD=postgres123
      - DB_PORT=5432
    volumes:
      - .:/app
    depends_on:
      - db
    networks:
      - app-network
    restart: unless-stopped

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: python_db
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

---

## Example 2: FastAPI with Redis and MongoDB

### Project Structure
```
fastapi-app/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── main.py
└── .env
```

### requirements.txt
```
fastapi==0.104.1
uvicorn==0.24.0
pymongo==4.6.2
redis==5.0.1
python-dotenv==1.0.0
aioredis==2.0.1
```

### main.py
```python
from fastapi import FastAPI
from pymongo import MongoClient
import redis
import os

app = FastAPI(title="FastAPI with Redis & MongoDB")

# MongoDB connection
mongo_uri = f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@mongo:27017/"
mongo_client = MongoClient(mongo_uri)
db = mongo_client[os.getenv('MONGO_DB', 'fastapi_db')]

# Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

@app.get("/")
async def read_root():
    return {"message": "FastAPI with Redis & MongoDB"}

@app.get("/health")
async def health_check():
    try:
        redis_client.ping()
        mongo_client.admin.command('ping')
        return {"status": "healthy", "redis": "connected", "mongodb": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/data")
async def create_data(data: dict):
    try:
        result = db.items.insert_one(data)
        redis_client.set(f"item:{result.inserted_id}", str(data))
        return {"id": str(result.inserted_id), "status": "created"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/data/{item_id}")
async def get_data(item_id: str):
    cached = redis_client.get(f"item:{item_id}")
    if cached:
        return {"source": "cache", "data": cached}
    
    from bson.objectid import ObjectId
    data = db.items.find_one({"_id": ObjectId(item_id)})
    if data:
        return {"source": "database", "data": str(data)}
    return {"error": "Not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### docker-compose.yml (Example 2)
```yaml
version: '3.8'

services:
  # FastAPI Application
  api:
    build: .
    container_name: fastapi_app
    ports:
      - "8000:8000"
    environment:
      - MONGO_HOST=mongo
      - MONGO_PORT=27017
      - MONGO_USER=admin
      - MONGO_PASSWORD=admin123
      - MONGO_DB=fastapi_db
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    volumes:
      - .:/app
      - /app/__pycache__
    depends_on:
      - mongo
      - redis
    networks:
      - app-network
    restart: unless-stopped
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  # MongoDB
  mongo:
    image: mongo:7.0
    container_name: fastapi_mongo
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=admin123
      - MONGO_INITDB_DATABASE=fastapi_db
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    networks:
      - app-network
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: fastapi_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped
    command: redis-server --appendonly yes

volumes:
  mongo_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

---

## Example 3: Full Stack - Django + PostgreSQL + Nginx

### Project Structure
```
django-app/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
├── nginx/
│   └── nginx.conf
└── myapp/
    └── settings.py
```

### requirements.txt
```
Django==4.2.0
psycopg2-binary==2.9.6
gunicorn==21.2.0
python-dotenv==1.0.0
```

### docker-compose.yml (Example 3)
```yaml
version: '3.8'

services:
  # Django Web Application
  web:
    build: .
    container_name: django_web
    command: gunicorn myapp.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/mediafiles
    environment:
      - DEBUG=False
      - ALLOWED_HOSTS=localhost,127.0.0.1,nginx
      - DB_ENGINE=django.db.backends.postgresql
      - DB_NAME=django_db
      - DB_USER=postgres
      - DB_PASSWORD=postgres123
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db
    networks:
      - app-network
    restart: unless-stopped

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: django_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=django_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres123
    ports:
      - "5432:5432"
    networks:
      - app-network
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: django_nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/mediafiles:ro
    ports:
      - "80:80"
    depends_on:
      - web
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
  media_volume:

networks:
  app-network:
    driver: bridge
```

### nginx.conf (Example 3)
```nginx
events {
    worker_connections 1024;
}

http {
    upstream django {
        server web:8000;
    }

    server {
        listen 80;
        server_name _;
        client_max_body_size 10M;

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/mediafiles/;
        }
    }
}
```

---

## Best Practices

### 1. Environment Variables
Always use `.env` files (don't commit them) instead of hardcoding values:

```yaml
services:
  app:
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
```

### 2. Resource Limits
Set limits to prevent containers from consuming excessive resources:

```yaml
services:
  web:
    build: .
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### 3. Health Checks
Add health checks to ensure services are running properly:

```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 4. Logging
Configure proper logging:

```yaml
services:
  web:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 5. Don't Run as Root
In Dockerfile, create a non-root user:

```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### 6. Proper Shutdown Handling
Use `stop_grace_period` to allow services to shut down gracefully:

```yaml
services:
  web:
    stop_grace_period: 30s
```

### 7. Networking
Use explicit networks instead of the default bridge:

```yaml
networks:
  app-network:
    driver: bridge
```

---

## Common Commands

### Start Services
```bash
# Start in foreground
docker-compose up

# Start in background
docker-compose up -d

# Rebuild images and start
docker-compose up --build
```

### Stop Services
```bash
# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove volumes as well
docker-compose down -v
```

### View Logs
```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
```

### Execute Commands
```bash
# Run command in service
docker-compose exec web python manage.py migrate

# Run command without starting dependencies
docker-compose run --rm web python manage.py shell
```

### Show Status
```bash
# List running services
docker-compose ps

# Show configuration
docker-compose config
```

### Rebuild and Clean
```bash
# Rebuild specific service
docker-compose build web

# Clean up unused images and volumes
docker system prune
```

---

## Troubleshooting

### Common Issues

**Issue: "Cannot connect to database"**
- Ensure `depends_on` is properly configured
- Use service name (not localhost) when connecting from another service
- Check environment variables are correctly set

**Issue: "Port already in use"**
```bash
# Change port in docker-compose.yml
ports:
  - "5001:5000"  # Use different host port
```

**Issue: "Permission denied" errors**
- Ensure file permissions are correct on mounted volumes
- Add `user:` directive in docker-compose.yml
- Run with proper ownership

**Issue: "Containers not communicating"**
- Verify all services are on the same network
- Use service name (not IP) for communication
- Check firewall settings

---

## Next Steps

1. Choose an example above based on your needs
2. Create the necessary files in your project directory
3. Run `docker-compose up` to start all services
4. Access your application at the configured port
5. Use `docker-compose logs` to debug issues

For more information, visit the [official Docker Compose documentation](https://docs.docker.com/compose/).

---

## Summary

Docker Compose simplifies multi-container application development by:
- Centralizing configuration in one file
- Automating service networking
- Enabling reproducible environments
- Speeding up development workflows

Start with the examples provided and customize them for your specific needs. With practice, Docker Compose will become an essential tool in your development workflow.
