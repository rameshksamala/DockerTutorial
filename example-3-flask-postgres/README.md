# Example 3 – Flask + PostgreSQL (Full Stack)

A complete Flask app connected to PostgreSQL using environment variables and named volumes for data persistence.

## How to Run

```bash
# 1. Copy the example environment file
cp .env.example .env

# 2. (Optional) Edit .env with your own values

# 3. Build and start
docker compose up --build
```

Then open: **http://localhost:5000**

## Routes to Try

| Route | What It Does |
|---|---|
| `/` | Shows PostgreSQL version (confirms connection) |
| `/create-table` | Creates a `messages` table |
| `/add-message` | Inserts a sample message |
| `/messages` | Lists all messages |

## How to Stop (keep data)

```bash
docker compose down
```

## How to Stop AND wipe the database

```bash
docker compose down -v    # WARNING: deletes the pgdata volume!
```

## Key Concepts Demonstrated

- **`.env` file** — secrets stay out of `docker-compose.yml`
- **Named volume `pgdata`** — database survives `docker compose down`
- **Health check** — `web` waits until PostgreSQL is actually ready
- **`depends_on: condition: service_healthy`** — robust startup ordering
- **Environment variables in app** — `os.environ['DB_HOST']` instead of hardcoded values

## Project Structure

```
example-3-flask-postgres/
├── app.py              # Flask app with PostgreSQL routes
├── requirements.txt    # Python dependencies
├── Dockerfile          # Build instructions for web image
├── docker-compose.yml  # Two services: web + db, with volume and health check
├── .env.example        # Template for environment variables (safe to commit)
├── .gitignore          # Prevents .env from being committed to Git
└── README.md
```

## Security Reminder

- ✅ Commit `.env.example` (template with no real secrets)
- ❌ Never commit `.env` (contains your real passwords)
- The `.gitignore` in this folder already protects you!
