# ─────────────────────────────────────────────────────────────
# Layer 1 · FROM — Base image
# Pulls the official slim Python 3.12 image from Docker Hub.
# 'slim' keeps the image small (~50 MB vs ~1 GB for full image).
# ─────────────────────────────────────────────────────────────
FROM python:3.12-slim

# ─────────────────────────────────────────────────────────────
# Layer 2 · ARG — Build-time variable
# Available only during the build process (docker build --build-arg).
# Not persisted in the final image unless forwarded to ENV.
# ─────────────────────────────────────────────────────────────
ARG BUILD_VERSION=1.0

# ─────────────────────────────────────────────────────────────
# Layer 3 · ENV — Runtime environment variables
# Persisted inside the image and available at container runtime.
# - PYTHONDONTWRITEBYTECODE  → no .pyc files
# - PYTHONUNBUFFERED         → print() output shows immediately
# ─────────────────────────────────────────────────────────────
ENV APP_ENV=production \
    APP_VERSION=${BUILD_VERSION} \
    APP_PORT=8080 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ─────────────────────────────────────────────────────────────
# Layer 4 · WORKDIR — Set working directory
# Creates /app if it doesn't exist; all subsequent commands
# (COPY, RUN, CMD) resolve paths relative to /app.
# ─────────────────────────────────────────────────────────────
WORKDIR /app

# ─────────────────────────────────────────────────────────────
# Layer 5 · COPY — Copy source files into the image
# Copy requirements first so Docker can cache the pip install
# layer separately — only re-runs when requirements.txt changes.
# ─────────────────────────────────────────────────────────────
COPY requirements.txt .
COPY app.py .

# ─────────────────────────────────────────────────────────────
# Layer 6 · RUN — Execute commands during build
# Each RUN creates a new image layer. Chaining commands with &&
# keeps related steps in one layer and reduces image size.
# - useradd creates a non-root user (used in Layer 9)
# - mkdir -p creates the data directory (used by VOLUME)
# ─────────────────────────────────────────────────────────────
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --shell /bin/bash appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appuser /app

# ─────────────────────────────────────────────────────────────
# Layer 7 · EXPOSE — Document the port the app listens on
# Informational only — actual port binding happens at runtime
# with: docker run -p 8080:8080 ...
# ─────────────────────────────────────────────────────────────
EXPOSE 8080

# ─────────────────────────────────────────────────────────────
# Layer 8 · VOLUME — Declare a persistent data mount point
# Data written to /app/data survives container restarts.
# Mount a host directory with: docker run -v mydata:/app/data ...
# ─────────────────────────────────────────────────────────────
VOLUME ["/app/data"]

# ─────────────────────────────────────────────────────────────
# Layer 9 · USER — Run as non-root for security
# Switch to the 'appuser' created in the RUN layer.
# Running as root inside a container is a security risk.
# ─────────────────────────────────────────────────────────────
USER appuser

# ─────────────────────────────────────────────────────────────
# Layer 10 · CMD — Default command to run on container start
# Use exec form ["python", "app.py"] (not shell form) so the
# Python process receives OS signals (SIGTERM) directly.
# ─────────────────────────────────────────────────────────────
CMD ["python", "app.py"]
