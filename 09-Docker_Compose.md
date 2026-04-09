# 🐳 Docker Compose for Beginners

A beginner-friendly, practical guide to Docker Compose with Python (Flask) examples.  
Everything you need to go from zero to running multi-container apps — in one repo.

---

## 📚 Table of Contents

- [What is Docker Compose?](#what-is-docker-compose)
- [Why Use It?](#why-use-it)
- [Core Concepts](#core-concepts)
- [Installation](#installation)
- [Anatomy of docker-compose.yml](#anatomy-of-docker-composeyml)
- [Examples](#examples)
  - [Example 1 – Hello World Flask](#example-1--hello-world-flask)
  - [Example 2 – Flask + Redis](#example-2--flask--redis-visit-counter)
  - [Example 3 – Flask + PostgreSQL](#example-3--flask--postgresql-full-stack)
- [Essential Commands](#essential-commands)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Cheat Sheet](#cheat-sheet)

---

## What is Docker Compose?

Docker Compose is a tool that lets you **define and run multi-container Docker applications**.

Instead of starting each container manually with long commands, you describe your entire application — all its services, networks, and volumes — in a single file called `docker-compose.yml`, and bring everything up with one command:

```bash
docker compose up
```

> 💡 Think of Docker as running individual programs. Docker Compose is like writing a script that starts all your programs together, automatically wired up and ready to talk to each other.

---

## Why Use It?

Without Docker Compose, running a web app + database requires you to:

1. Start the database container manually
2. Start the web app container manually
3. Link them together with network flags
4. Mount volumes by hand
5. Remember all the options every single time

With Docker Compose, you write this **once** in a YAML file and run `docker compose up`. Done.

**Key benefits:**
- ✅ Single command to start or stop your entire application
- ✅ Easy to share — anyone can clone and run it
- ✅ Consistent across dev, test, and production
- ✅ Service isolation: each piece runs in its own container
- ✅ Built-in networking between containers

---

## Core Concepts

| Concept | What It Means |
|---|---|
| **Service** | One container in your app (e.g., web, db, cache) |
| **Image** | Blueprint for a container (pulled from Docker Hub) |
| **Port** | Maps `HOST:CONTAINER` so you can access the container |
| **Volume** | Persists data on your machine across restarts |
| **Network** | Auto-created private network; services talk by service name |
| **Environment Variable** | Config values (passwords, modes) passed into containers |

---

## Installation

Docker Compose ships with **Docker Desktop**.

1. Download Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Verify installation:

```bash
docker --version
# Docker version 24.x.x

docker compose version
# Docker Compose version v2.x.x
```

> 💡 On older versions you may see `docker-compose` (with a hyphen). Modern Docker uses `docker compose` (with a space).

---

## Anatomy of docker-compose.yml

```yaml
version: '3.8'                 # Compose file format version

services:                      # Define all containers here

  web:                         # Service name (you choose this)
    build: .                   # Build from Dockerfile in current directory
    ports:
      - '5000:5000'            # HOST:CONTAINER port mapping
    environment:
      - FLASK_ENV=development  # Environment variables inside the container
    volumes:
      - .:/app                 # Mount current dir to /app inside the container
    depends_on:
      - db                     # Start db service before web

  db:                          # Another service: PostgreSQL database
    image: postgres:15         # Use the official PostgreSQL image
    environment:
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=myapp
    volumes:
      - db_data:/var/lib/postgresql/data   # Named volume for persistence

volumes:
  db_data:                     # Declare named volumes here
```

**YAML Rules to Remember:**
- Use **spaces** (2 or 4), never tabs
- Each nested level adds more indentation
- `services`, `volumes`, and `networks` are at the top level

---

## Examples

### Example 1 – Hello World Flask

The simplest possible example: a Flask web app in Docker.

📁 [`example-1-hello-flask/`](./example-1-hello-flask/)

```bash
cd example-1-hello-flask
docker compose up
```

Visit → http://localhost:5000

---

### Example 2 – Flask + Redis (Visit Counter)

Two services communicating: Flask stores visit counts in Redis.

📁 [`example-2-flask-redis/`](./example-2-flask-redis/)

```bash
cd example-2-flask-redis
docker compose up --build
```

Visit → http://localhost:5000 and refresh the page. The counter increments!

> 💡 Flask connects to Redis using `host='redis'` — the service name. Docker Compose auto-creates DNS entries for each service.

---

### Example 3 – Flask + PostgreSQL (Full Stack)

Full-stack app: Flask + PostgreSQL with environment variables and persistent data.

📁 [`example-3-flask-postgres/`](./example-3-flask-postgres/)

```bash
cd example-3-flask-postgres
cp .env.example .env   # Copy and edit environment variables
docker compose up --build
```

Visit → http://localhost:5000

---

## Essential Commands

Run all commands from the directory containing your `docker-compose.yml`.

| Command | What It Does |
|---|---|
| `docker compose up` | Start all services (attached to logs) |
| `docker compose up -d` | Start all services in background (detached) |
| `docker compose up --build` | Rebuild images before starting |
| `docker compose down` | Stop and remove containers + networks |
| `docker compose down -v` | Also remove volumes (**wipes data!**) |
| `docker compose ps` | List running services |
| `docker compose logs` | Show logs from all services |
| `docker compose logs web` | Show logs from a specific service |
| `docker compose logs -f` | Follow logs in real time |
| `docker compose exec web bash` | Open a shell inside a running container |
| `docker compose restart web` | Restart a specific service |
| `docker compose build` | Build/rebuild images without starting |
| `docker compose pull` | Pull latest images from Docker Hub |
| `docker compose stop` | Stop services (without removing them) |
| `docker compose start` | Start previously stopped services |

---

## Troubleshooting

### Port Already in Use
```
Error: Bind for 0.0.0.0:5000 failed: port is already allocated
```
**Fix:** Change the host port in `docker-compose.yml`. E.g., `'5001:5000'`

---

### Service Not Ready (`depends_on` Limitation)
`depends_on` only waits for the container to **start**, not for the service inside to be ready (e.g., PostgreSQL takes a few seconds to init).

**Fix:** Add a health check:
```yaml
db:
  image: postgres:15
  healthcheck:
    test: ['CMD-SHELL', 'pg_isready -U admin']
    interval: 5s
    timeout: 5s
    retries: 5
```

---

### Changes Not Reflecting
Rebuild your image after changing code:
```bash
docker compose up --build
```

---

### Cannot Connect Between Services
Use the **service name** as the hostname, not `localhost`.

```python
# ✅ Correct
r = redis.Redis(host='redis', port=6379)

# ❌ Wrong
r = redis.Redis(host='localhost', port=6379)
```

---

## Best Practices

- 🔐 Use a `.env` file for secrets — never hardcode passwords in `docker-compose.yml`
- 🚫 Add `.env` to `.gitignore` — never commit secrets to Git
- 💾 Use named volumes for important data so it survives `docker compose down`
- 🪶 Use `alpine` image variants (e.g., `redis:7-alpine`) for smaller containers
- 🏷️ Pin specific image versions (e.g., `postgres:15`) — avoid `:latest`
- 📋 Use `docker compose logs -f` during development
- 🧪 Use health checks for services with startup delays
- 🗃️ Keep `Dockerfile` and `docker-compose.yml` in version control

---

## Cheat Sheet

### Minimal docker-compose.yml Template

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - 'HOST_PORT:CONTAINER_PORT'
    environment:
      - KEY=value
    volumes:
      - ./local:/container/path
    depends_on:
      - db
  db:
    image: IMAGE_NAME:TAG
    environment:
      - KEY=value
    volumes:
      - datavolume:/data/path
volumes:
  datavolume:
```

### Common Base Images

| Image | Use Case |
|---|---|
| `python:3.11-slim` | Python apps |
| `node:20-alpine` | Node.js apps |
| `postgres:15` | PostgreSQL database |
| `mysql:8.0` | MySQL database |
| `redis:7-alpine` | Redis cache / queue |
| `nginx:alpine` | Reverse proxy / static files |
| `mongo:7` | MongoDB database |

---

## 📄 License

MIT — free to use, share, and modify.

---

## 🙌 Contributing

Found a bug or want to add an example? Open an issue or pull request!

---

*Happy Composing! 🐳*
