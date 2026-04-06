# 🐳 What is a Docker Image?

A comprehensive guide to understanding Docker images, layers, and containers.

---

## Table of Contents

- [What is a Docker Image?](#1-what-is-a-docker-image)
- [Image Properties](#image-properties)
- [Image vs Container](#image-vs-container)
- [Understanding Layers](#2-understanding-layers)
- [The Container Layer](#3-the-container-layer-readwrite)
- [Useful Commands Reference](#useful-commands-reference)
- [Example Dockerfile](#example-dockerfile)

---

## 1. What is a Docker Image?

A Docker image is a **read-only, immutable template** used to create containers. It packages everything an application needs to run — from the operating system base all the way up to the application code — into a portable, self-contained unit.

> 💡 Think of an image as a **blueprint** and a container as a **running instance** built from that blueprint.

---

## Image Properties

| Property | Description |
|----------|-------------|
| **Read-only** | Layers cannot be changed after creation |
| **Portable** | The same image runs identically on any Docker host |
| **Layered** | Built from a stack of incremental filesystem snapshots |
| **Versioned** | Tagged with names like `ubuntu:22.04` or `my-app:1.0.3` |
| **Shareable** | Stored in and distributed from image registries |

---

## Image vs Container

| Concept | Image | Container |
|---------|-------|-----------|
| **Analogy** | Blueprint / Class definition | Running instance / Object |
| **State** | Static, stored on disk | Dynamic, lives in memory |
| **Mutability** | Read-only | Has a thin read/write layer on top |
| **Lifespan** | Persistent until deleted | Ephemeral — deleted with `docker rm` |
| **Command** | `docker build` / `docker pull` | `docker run` |

---

## 2. Understanding Layers

A Docker image is **not a single monolithic file**. It is a stack of read-only layers, where each layer represents a delta (incremental change) to the filesystem produced by one instruction in a `Dockerfile`.

> ⚠️ Every `RUN`, `COPY`, and `ADD` instruction in a Dockerfile creates a new layer. `FROM`, `ENV`, `CMD`, `EXPOSE`, and `LABEL` create metadata but do **not** add filesystem layers.

### Layer Stack — How It Looks

Layers stack from bottom (base) to top (application), each one only storing the changes from the layer below:

```
┌─────────────────────────────────────────────┐
│  Layer 5 (TOP) — CMD ["python3", "app.py"]  │  ← metadata / entrypoint
├─────────────────────────────────────────────┤
│  Layer 4 — pip install -r requirements.txt  │  ← Python packages
├─────────────────────────────────────────────┤
│  Layer 3 — COPY app.py /app/                │  ← your application code
├─────────────────────────────────────────────┤
│  Layer 2 — RUN apt-get install python3      │  ← runtime packages
├─────────────────────────────────────────────┤
│  Layer 1 (BASE) — FROM ubuntu:22.04         │  ← base OS filesystem
└─────────────────────────────────────────────┘
```

### What Each Layer Stores

| Dockerfile Instruction | Creates Layer? | What is Stored |
|------------------------|----------------|----------------|
| `FROM` | ✅ Yes (base) | Full base image filesystem |
| `RUN` | ✅ Yes | Files added/changed by the command (packages, compiled code) |
| `COPY` / `ADD` | ✅ Yes | Files copied from build context into the image |
| `ENV` | ❌ No (metadata) | Environment variable stored in image config |
| `EXPOSE` | ❌ No (metadata) | Port hint stored in image config only |
| `CMD` / `ENTRYPOINT` | ❌ No (metadata) | Default command stored in image config |

---

## 3. The Container Layer (Read/Write)

When you run `docker run`, Docker does **not** modify the image. Instead, it adds a thin, writable **container layer** on top of all the read-only image layers. All writes during the container's lifetime go into this layer.

### Full Layer Stack at Runtime

```
┌──────────────────────────────────────────────────────────────┐
│  Container Layer (top)   │  Read/Write  │ Created per        │
│                          │              │ container; deleted  │
│                          │              │ with docker rm      │
├──────────────────────────┼──────────────┼────────────────────┤
│  Layer 5 — CMD metadata  │  Read-Only   │ Shared across all  │
│  Layer 4 — pip install   │  Read-Only   │ containers using   │
│  Layer 3 — COPY app.py   │  Read-Only   │ this image         │
│  Layer 2 — apt-get       │  Read-Only   │                    │
│  Layer 1 — Base OS       │  Read-Only   │                    │
└──────────────────────────┴──────────────┴────────────────────┘
```

---

## Useful Commands Reference

| Command | What it Does |
|---------|-------------|
| `docker images` | List all local images |
| `docker history <image>` | Show all layers and their sizes |
| `docker inspect <image>` | Show full image metadata in JSON |
| `docker pull <image>` | Download image from registry |
| `docker push <image>` | Upload image to registry |
| `docker rmi <image>` | Remove a local image |
| `docker system prune` | Remove all unused images, containers, networks |
| `docker build --no-cache` | Force full rebuild, ignoring cache |
| `docker build -t name:tag .` | Build image from Dockerfile in current directory |

---

## Example Dockerfile

See [`examples/Dockerfile`](examples/Dockerfile) for a sample Python app Dockerfile that demonstrates the layering concepts described in this guide.

---

## Further Reading

- [Docker Official Documentation](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Image Layers Explained](https://docs.docker.com/storage/storagedriver/)
