# 🔍 Container Concepts In Depth

This document expands on the core ideas introduced in the main README.

---

## What Lives Inside a Container?

A container bundles the following:

| Component | Examples |
|-----------|----------|
| **Application code** | `.js`, `.py`, `.java` files |
| **Runtime** | Node.js 18, Python 3.11, JVM 17 |
| **System libraries** | `glibc`, `openssl`, `zlib` |
| **Environment variables** | `DATABASE_URL`, `API_KEY` |
| **Configuration** | `nginx.conf`, `app.yaml` |

---

## Container vs Image

| Concept | Analogy | Description |
|---------|---------|-------------|
| **Image** | Blueprint / Class | Read-only template built from a Dockerfile |
| **Container** | Running Instance / Object | A live, running process from an image |

---

## Container Isolation

Containers use Linux kernel features for isolation:

- **Namespaces** — isolate process IDs, networking, filesystems
- **cgroups** (control groups) — limit CPU, memory, I/O usage
- **Union filesystems** (OverlayFS) — layered, efficient image storage

---

## Container Lifecycle

```
docker build   →   Image created
docker push    →   Image pushed to registry
docker pull    →   Image pulled to host
docker run     →   Container started
docker stop    →   Container stopped (state preserved)
docker rm      →   Container removed
docker rmi     →   Image removed
```

---

## Port Mapping

Containers have their own network namespace. Use port mapping to expose services:

```bash
# Host port 8080 → Container port 3000
docker run -p 8080:3000 my-app
```

---

## Environment Variables

Pass config at runtime — no need to bake secrets into images:

```bash
docker run -e DATABASE_URL=postgres://... -e NODE_ENV=production my-app
```

---

## Volumes — Persisting Data

Containers are ephemeral. Use volumes to keep data alive across restarts:

```bash
# Named volume
docker run -v my-data:/app/data my-app

# Bind mount (local folder ↔ container folder)
docker run -v $(pwd)/data:/app/data my-app
```

---

## Networking Modes

| Mode | Description |
|------|-------------|
| `bridge` (default) | Containers on a private virtual network |
| `host` | Container shares the host network stack |
| `none` | No networking |
| `overlay` | Multi-host networking (used with Swarm/K8s) |

---

## Key Docker CLI Commands

```bash
# Build an image
docker build -t my-app:1.0 .

# Run a container (detached, with port mapping)
docker run -d -p 8080:3000 --name my-container my-app:1.0

# List running containers
docker ps

# View logs
docker logs my-container

# Open a shell inside a running container
docker exec -it my-container sh

# Stop and remove
docker stop my-container
docker rm my-container

# Remove image
docker rmi my-app:1.0
```
