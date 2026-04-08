# 🐳 Docker Fundamentals — Dockerfile Layers & Docker Hub Guide

> A complete walkthrough of all 10 Dockerfile layers with a Python verification script and step-by-step Docker Hub publishing instructions.

---

## 📋 Table of Contents

- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Dockerfile Layers — Deep Dive](#-dockerfile-layers--deep-dive)
  - [Layer 1 — FROM](#layer-1--from--base-image)
  - [Layer 2 — ARG](#layer-2--arg--build-time-variable)
  - [Layer 3 — ENV](#layer-3--env--runtime-environment-variables)
  - [Layer 4 — WORKDIR](#layer-4--workdir--working-directory)
  - [Layer 5 — COPY](#layer-5--copy--copy-files-into-the-image)
  - [Layer 6 — RUN](#layer-6--run--execute-commands-at-build-time)
  - [Layer 7 — EXPOSE](#layer-7--expose--declare-the-listening-port)
  - [Layer 8 — VOLUME](#layer-8--volume--persistent-data-mount)
  - [Layer 9 — USER](#layer-9--user--non-root-security)
  - [Layer 10 — CMD](#layer-10--cmd--default-startup-command)
- [Python Verification Script](#-python-verification-script)
- [Build & Run Scenarios](#-build--run-scenarios)
- [Pushing to Docker Hub](#-pushing-to-docker-hub)
- [GitHub Actions — Auto Push](#-github-actions--auto-push)
- [Quick Reference](#-quick-reference)
- [Troubleshooting](#-troubleshooting)

---

## 📁 Project Structure

```
.
├── Dockerfile          # Image build instructions (all 10 layers)
├── app.py              # Python script — verifies each layer at runtime
└── requirements.txt    # Pip packages installed by the RUN layer
```

---

## ✅ Prerequisites

| Requirement | Version | Check |
|---|---|---|
| Docker Desktop / Engine | 24.x+ | `docker --version` |
| Python (local dev only) | 3.12+ | `python --version` |
| Docker Hub account | Free tier | [hub.docker.com](https://hub.docker.com) |

---

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. Build the image
docker build --build-arg BUILD_VERSION=1.0 -t my-python-app .

# 3. Run with volume + port binding
docker run -v mydata:/app/data -p 8080:8080 my-python-app
```

Expected output:

```
╔══════════════════════════════════════════════════════╗
║        Docker Layer Verification Report              ║
╚══════════════════════════════════════════════════════╝
  2025-01-01 10:00:00 UTC

──────────────────────────────────────────────────────
  Layer 1 · FROM — Base image
──────────────────────────────────────────────────────
  ✔  OS                           Linux
  ✔  Python version               3.12.x
  ...
══════════════════════════════════════════════════════
  All 10 Dockerfile layers verified!
══════════════════════════════════════════════════════
```

---

## 🔍 Dockerfile Layers — Deep Dive

Below is the complete `Dockerfile` followed by a detailed explanation of every layer.

```dockerfile
# Layer 1 · FROM
FROM python:3.12-slim

# Layer 2 · ARG
ARG BUILD_VERSION=1.0

# Layer 3 · ENV
ENV APP_ENV=production \
    APP_VERSION=${BUILD_VERSION} \
    APP_PORT=8080 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Layer 4 · WORKDIR
WORKDIR /app

# Layer 5 · COPY
COPY requirements.txt .
COPY app.py .

# Layer 6 · RUN
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --shell /bin/bash appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appuser /app

# Layer 7 · EXPOSE
EXPOSE 8080

# Layer 8 · VOLUME
VOLUME ["/app/data"]

# Layer 9 · USER
USER appuser

# Layer 10 · CMD
CMD ["python", "app.py"]
```

---

### Layer 1 — FROM — Base Image

```dockerfile
FROM python:3.12-slim
```

**What it does:** Pulls the official Python 3.12 slim image from Docker Hub as the foundation. Every subsequent layer stacks on top of this.

| Variant | Size | Use case |
|---|---|---|
| `python:3.12` | ~1 GB | Full Debian — maximum compatibility |
| `python:3.12-slim` | ~50 MB | Minimal Debian — recommended for most apps |
| `python:3.12-alpine` | ~20 MB | Alpine Linux — smallest, but some packages need extra setup |

> 💡 **Tip:** Prefer `slim` over the full image for smaller attack surface and faster pulls. Use `alpine` only if you need the absolute minimum size and are comfortable resolving C extension issues.

---

### Layer 2 — ARG — Build-Time Variable

```dockerfile
ARG BUILD_VERSION=1.0
```

**What it does:** Declares a variable that exists **only during `docker build`**. It is not available at runtime unless explicitly forwarded to `ENV`.

**Scenario — passing a version at build time:**

```bash
# Use the default (1.0)
docker build -t my-python-app .

# Override with a specific version
docker build --build-arg BUILD_VERSION=2.5 -t my-python-app .

# Verify the value was baked in
docker inspect my-python-app | grep APP_VERSION
```

> ⚠️ **Security note:** Do not use `ARG` for secrets (passwords, tokens). ARG values are visible in `docker history`. Use runtime secrets or Docker BuildKit secrets instead.

---

### Layer 3 — ENV — Runtime Environment Variables

```dockerfile
ENV APP_ENV=production \
    APP_VERSION=${BUILD_VERSION} \
    APP_PORT=8080 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```

**What it does:** Sets key-value pairs that are persisted in the image and available to every process inside the container.

| Variable | Value | Purpose |
|---|---|---|
| `APP_ENV` | `production` | Application environment flag |
| `APP_VERSION` | `${BUILD_VERSION}` | Forwards the ARG into runtime |
| `APP_PORT` | `8080` | Port the app listens on |
| `PYTHONDONTWRITEBYTECODE` | `1` | Prevents `.pyc` file creation |
| `PYTHONUNBUFFERED` | `1` | Ensures `print()` output appears immediately |

**Scenario — override ENV at runtime (without rebuilding):**

```bash
# Run in staging mode
docker run -e APP_ENV=staging my-python-app

# Run on a different port
docker run -e APP_PORT=9090 my-python-app

# Load from a .env file
docker run --env-file .env my-python-app
```

---

### Layer 4 — WORKDIR — Working Directory

```dockerfile
WORKDIR /app
```

**What it does:** Sets the working directory for all subsequent `RUN`, `COPY`, `CMD`, and `ENTRYPOINT` instructions. Creates the directory if it does not exist.

**Scenario — verify the working directory inside a running container:**

```bash
docker run --rm my-python-app pwd
# Output: /app

docker run --rm -it my-python-app bash
# You land directly in /app
```

> 💡 **Tip:** Always use `WORKDIR` instead of `RUN cd /some/path`. `WORKDIR` is explicit, predictable, and creates the directory automatically.

---

### Layer 5 — COPY — Copy Files into the Image

```dockerfile
COPY requirements.txt .
COPY app.py .
```

**What it does:** Transfers files from the host build context into the image filesystem at the `WORKDIR` path.

**Why `requirements.txt` is copied first:**

Docker builds layers in order and caches each one. If `requirements.txt` hasn't changed, the pip install layer is reused from cache — saving significant build time.

```
Build 1 (cold):       Build 2 (app.py changed):
  COPY requirements → cached  ✔
  RUN pip install   → cached  ✔  (saves ~30s)
  COPY app.py       → rebuilt ✗
  CMD               → rebuilt ✗
```

**Scenario — COPY with a `.dockerignore` file:**

Create `.dockerignore` to exclude unnecessary files:

```
# .dockerignore
__pycache__/
*.pyc
.env
.git
.venv
tests/
*.md
```

```bash
# Verify what was copied
docker run --rm my-python-app ls -la /app
```

---

### Layer 6 — RUN — Execute Commands at Build Time

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --shell /bin/bash appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appuser /app
```

**What it does:** Executes shell commands and commits the result as a new image layer. Commands are chained with `&&` to keep everything in a single layer, reducing image size.

| Command | Purpose |
|---|---|
| `pip install --no-cache-dir` | Install packages without caching to keep image small |
| `useradd ...` | Create a non-root user (used in Layer 9) |
| `mkdir -p /app/data` | Create the data directory (used by VOLUME) |
| `chown -R appuser:appuser /app` | Give appuser ownership of all app files |

**Scenario — inspect installed packages inside the image:**

```bash
docker run --rm my-python-app pip list
```

**Scenario — check image layer sizes:**

```bash
docker history my-python-app
```

> 💡 **Best practice:** Chain all related commands in a single `RUN` with `&&`. Each `RUN` instruction creates a separate layer. Splitting them unnecessarily bloats the image.

---

### Layer 7 — EXPOSE — Declare the Listening Port

```dockerfile
EXPOSE 8080
```

**What it does:** Documents that the container listens on port 8080. This is **informational only** — it does not publish the port to the host.

**Scenario — bind the port at runtime:**

```bash
# Map host port 8080 → container port 8080
docker run -p 8080:8080 my-python-app

# Map to a different host port
docker run -p 9090:8080 my-python-app

# Publish all exposed ports to random host ports
docker run -P my-python-app

# Check what ports are mapped
docker port <container_id>
```

---

### Layer 8 — VOLUME — Persistent Data Mount

```dockerfile
VOLUME ["/app/data"]
```

**What it does:** Declares `/app/data` as a persistent mount point. Data written here survives container restarts and can be shared between containers.

**Scenario — named volume (recommended for production):**

```bash
# Create and mount a named volume
docker run -v mydata:/app/data my-python-app

# Inspect the volume
docker volume inspect mydata

# List all volumes
docker volume ls
```

**Scenario — bind mount (good for local development):**

```bash
# Mount a host directory directly
docker run -v $(pwd)/data:/app/data my-python-app

# Changes on the host are immediately visible inside the container
```

**Scenario — share a volume between two containers:**

```bash
# Container 1 writes
docker run -d -v sharedvol:/app/data --name writer my-python-app

# Container 2 reads the same data
docker run -v sharedvol:/app/data --name reader my-python-app cat /app/data/volume_test.json
```

> ⚠️ **Note:** If you don't mount a volume with `-v`, Docker creates an anonymous volume automatically. Use `docker volume prune` periodically to clean up orphaned volumes.

---

### Layer 9 — USER — Non-Root Security

```dockerfile
USER appuser
```

**What it does:** Switches the running process from `root` to `appuser` (created in the `RUN` layer). Running as root inside a container is a significant security risk.

**Scenario — verify the user context:**

```bash
# Check which user the container runs as
docker run --rm my-python-app whoami
# Output: appuser

# Check UID/GID
docker run --rm my-python-app id
# Output: uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
```

**Scenario — temporarily run as root for debugging:**

```bash
docker run --rm -u root -it my-python-app bash
```

> 🔒 **Security tip:** Never run production containers as root. A compromised root container can escape to the host. Always create a dedicated application user in `RUN` and switch with `USER` before `CMD`.

---

### Layer 10 — CMD — Default Startup Command

```dockerfile
CMD ["python", "app.py"]
```

**What it does:** Specifies the default command when the container starts. Uses **exec form** (JSON array) so the Python process receives OS signals like `SIGTERM` directly, enabling graceful shutdown.

| Form | Example | Signal handling |
|---|---|---|
| Exec (recommended) | `["python", "app.py"]` | Python receives SIGTERM directly ✅ |
| Shell | `python app.py` | Signals go to shell, not Python ❌ |

**Scenario — override CMD at runtime:**

```bash
# Run a different command instead
docker run my-python-app python --version

# Open an interactive shell
docker run -it my-python-app bash

# Run a one-off script
docker run my-python-app python -c "print('hello')"
```

**Scenario — use ENTRYPOINT with CMD for flexible containers:**

```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]          # default: python app.py
```

```bash
# Default run
docker run my-python-app              # runs: python app.py

# Override CMD only
docker run my-python-app other.py     # runs: python other.py
```

---

## 🐍 Python Verification Script

`app.py` runs a colour-coded health check against every layer when the container starts.

| Section | What it checks |
|---|---|
| **Layer 1 — FROM** | OS name, architecture, Python version and path |
| **Layer 2 — ARG** | `BUILD_VERSION` present in environment |
| **Layer 3 — ENV** | `APP_ENV`, `APP_PORT`, `PYTHONUNBUFFERED` and others |
| **Layer 4 — WORKDIR** | `os.getcwd() == '/app'` |
| **Layer 5 — COPY** | `app.py` and `requirements.txt` exist with correct sizes |
| **Layer 6 — RUN** | `requests`, `flask`, `psutil` successfully importable |
| **Layer 7 — EXPOSE** | Container hostname, IP, and `APP_PORT` value |
| **Layer 8 — VOLUME** | `/app/data` exists; writes a JSON test file |
| **Layer 9 — USER** | `os.getuid() != 0` (not root) |
| **Layer 10 — CMD** | PID, CPU count, memory total and available via psutil |

Output key:

```
✔  green  — layer verified correctly
⚠  yellow — layer present but misconfigured or optional item missing
✘  red    — layer check failed
```

---

## 🧪 Build & Run Scenarios

### Scenario 1 — Basic build and run

```bash
docker build -t my-python-app .
docker run my-python-app
```

### Scenario 2 — Build with a custom version

```bash
docker build --build-arg BUILD_VERSION=2.0 -t my-python-app:2.0 .
docker run my-python-app:2.0
```

### Scenario 3 — Run with persistent storage

```bash
docker run -v mydata:/app/data my-python-app

# Confirm data was written
docker run -v mydata:/app/data --rm my-python-app \
  cat /app/data/volume_test.json
```

### Scenario 4 — Override environment variables at runtime

```bash
docker run \
  -e APP_ENV=staging \
  -e APP_PORT=9090 \
  my-python-app
```

### Scenario 5 — Open an interactive shell for debugging

```bash
docker run -it --rm my-python-app bash
# You are now inside the container at /app as appuser
```

### Scenario 6 — Run as root for emergency debugging

```bash
docker run -it --rm -u root my-python-app bash
```

### Scenario 7 — Check image size and layers

```bash
docker images my-python-app
docker history my-python-app --no-trunc
```

### Scenario 8 — Remove all stopped containers and unused images

```bash
docker container prune
docker image prune
# Nuclear option — remove everything unused
docker system prune -a
```

---

## 🚀 Pushing to Docker Hub

### Step 1 — Create a Docker Hub account

Sign up at [hub.docker.com](https://hub.docker.com) (free). Note your **username** — it becomes part of every image name you push.

---

### Step 2 — Log in from the terminal

```bash
docker login
```

Enter your Docker Hub username and password when prompted.

```
Username: yourusername
Password: ••••••••••
Login Succeeded
```

> 💡 **Tip:** Use an **Access Token** instead of your password for better security. Generate one at: Docker Hub → Account Settings → Security → New Access Token.

```bash
# Login with a token
docker login -u yourusername
# Paste your access token when prompted for the password
```

---

### Step 3 — Tag the image

Docker Hub expects image names in the format `username/repository:tag`.

```bash
# Tag with a version
docker tag my-python-app yourusername/my-python-app:1.0

# Also tag as latest
docker tag my-python-app yourusername/my-python-app:latest
```

**Tagging strategy:**

| Tag | Example | When to use |
|---|---|---|
| `latest` | `user/app:latest` | Always points to the most recent push |
| Semantic version | `user/app:1.0` | Stable release — increment for each change |
| Patch version | `user/app:1.0.3` | Bug fix within a minor version |
| `dev` | `user/app:dev` | Development build — never use in production |
| Git SHA | `user/app:abc1234` | Exact traceability to a commit |

---

### Step 4 — Push to Docker Hub

```bash
# Push the versioned tag
docker push yourusername/my-python-app:1.0

# Push the latest tag
docker push yourusername/my-python-app:latest
```

Output:

```
The push refers to repository [docker.io/yourusername/my-python-app]
a1b2c3d4e5f6: Pushed
...
1.0: digest: sha256:abc123... size: 1234
```

---

### Step 5 — Verify the push

```bash
# Pull from Docker Hub on any machine
docker pull yourusername/my-python-app:1.0

# Run directly from Docker Hub (no local build needed)
docker run yourusername/my-python-app:1.0
```

---

### Step 6 — Full push workflow at a glance

```bash
# 1. Build
docker build --build-arg BUILD_VERSION=1.0 -t my-python-app .

# 2. Login
docker login

# 3. Tag
docker tag my-python-app yourusername/my-python-app:1.0
docker tag my-python-app yourusername/my-python-app:latest

# 4. Push
docker push yourusername/my-python-app:1.0
docker push yourusername/my-python-app:latest

# 5. Verify
docker pull yourusername/my-python-app:1.0
```

---

### Making the repository private

1. Log in to [hub.docker.com](https://hub.docker.com)
2. Navigate to your repository (`yourusername/my-python-app`)
3. Go to **Settings** → **Visibility**
4. Select **Private** and save

> ℹ️ The free Docker Hub plan includes **one private repository**. Additional private repositories require a paid plan.

---

## ⚙️ GitHub Actions — Auto Push

Automate building and pushing on every commit to `main`. Create the file below in your repository:

```yaml
# .github/workflows/docker.yml
name: Build and Push to Docker Hub

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source
        uses: actions/checkout@v4

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata (tags, labels)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ secrets.DOCKERHUB_USERNAME }}/my-python-app
          tags: |
            type=semver,pattern={{version}}
            type=ref,event=branch
            type=sha,prefix=git-

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          build-args: |
            BUILD_VERSION=${{ github.ref_name }}
```

**Add GitHub Secrets:**

1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Add `DOCKERHUB_USERNAME` → your Docker Hub username
3. Add `DOCKERHUB_TOKEN` → your Docker Hub access token

---

## 📖 Quick Reference

### Build commands

| Command | Description |
|---|---|
| `docker build -t name .` | Build image from Dockerfile in current directory |
| `docker build --build-arg K=V -t name .` | Build with a custom ARG value |
| `docker build --no-cache -t name .` | Build without using layer cache |
| `docker build -f MyDockerfile -t name .` | Build from a non-default Dockerfile name |

### Run commands

| Command | Description |
|---|---|
| `docker run name` | Start a container |
| `docker run -p 8080:8080 name` | Map host port → container port |
| `docker run -v vol:/app/data name` | Mount a named volume |
| `docker run -e KEY=VAL name` | Override an environment variable |
| `docker run --rm name` | Remove container automatically on exit |
| `docker run -it name bash` | Open an interactive shell |
| `docker run -d name` | Run container in the background |

### Inspect & debug

| Command | Description |
|---|---|
| `docker images` | List all local images |
| `docker ps -a` | List all containers (running + stopped) |
| `docker logs <id>` | View container stdout/stderr |
| `docker exec -it <id> bash` | Open a shell in a running container |
| `docker inspect <id>` | Full container or image metadata (JSON) |
| `docker history name` | Show image layer sizes |
| `docker stats` | Live resource usage of running containers |

### Docker Hub

| Command | Description |
|---|---|
| `docker login` | Authenticate with Docker Hub |
| `docker tag name user/name:tag` | Tag an image for pushing |
| `docker push user/name:tag` | Upload image to Docker Hub |
| `docker pull user/name:tag` | Download image from Docker Hub |
| `docker search <term>` | Search Docker Hub from the CLI |

### Cleanup

| Command | Description |
|---|---|
| `docker stop <id>` | Gracefully stop a running container |
| `docker rm <id>` | Remove a stopped container |
| `docker rmi name` | Remove a local image |
| `docker container prune` | Remove all stopped containers |
| `docker image prune` | Remove dangling images |
| `docker volume prune` | Remove unused volumes |
| `docker system prune -a` | Remove everything unused |

---

## 🔧 Troubleshooting

### Permission denied on `/app/data`

```
PermissionError: [Errno 13] Permission denied: '/app/data/volume_test.json'
```

**Cause:** The `chown` in the `RUN` layer didn't run, or a bind-mounted directory has incorrect host permissions.

```bash
# Fix: rebuild the image so chown is applied
docker build --no-cache -t my-python-app .

# For bind mounts, fix host directory permissions
chmod 777 ./data
```

---

### Port already in use

```
Error: bind: address already in use
```

**Cause:** Another process is using port 8080 on the host.

```bash
# Find what's using port 8080
lsof -i :8080        # macOS / Linux
netstat -ano | findstr :8080   # Windows

# Use a different host port instead
docker run -p 9090:8080 my-python-app
```

---

### Package not found — `pip install` fails

```
ERROR: Could not find a version that satisfies the requirement flask==3.1.0
```

**Cause:** Package version doesn't exist or network is unavailable.

```bash
# Remove the pinned version to get the latest
# requirements.txt:  flask   (instead of flask==3.1.0)

# Rebuild without cache
docker build --no-cache -t my-python-app .
```

---

### `docker push` access denied

```
denied: requested access to the resource is denied
```

**Cause:** Not logged in, or the image tag doesn't match your Docker Hub username.

```bash
# Re-login
docker login

# Ensure the tag includes your username
docker tag my-python-app yourusername/my-python-app:1.0
docker push yourusername/my-python-app:1.0
```

---

### Container exits immediately

```bash
# Check exit code and logs
docker ps -a
docker logs <container_id>

# Run interactively to see the error
docker run -it my-python-app bash
```

---

<div align="center">

Made with ❤️ to learn Docker fundamentals

</div>
