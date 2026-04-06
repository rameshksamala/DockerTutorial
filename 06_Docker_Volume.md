# 🐳 Docker Storage Management
### Volumes, Bind Mounts & Persistent Data — A Comprehensive Reference Guide

---

## 📋 Table of Contents

- [1. Introduction to Docker Storage](#1-introduction-to-docker-storage)
- [2. Docker Volumes](#2-docker-volumes)
  - [2.1 Volume Types](#21-volume-types)
  - [2.2 Volume Management Commands](#22-volume-management-commands)
  - [2.3 Mounting Named Volumes to Containers](#23-mounting-named-volumes-to-containers)
- [3. Bind Mounts](#3-bind-mounts)
  - [3.1 Syntax](#31-syntax)
  - [3.2 Example — Nginx with Bind Mount](#32-example--nginx-with-bind-mount)
  - [3.3 Use Cases for Bind Mounts](#33-use-cases-for-bind-mounts)
- [4. Read-Only Volumes](#4-read-only-volumes)
- [5. Volumes vs Bind Mounts — Comparison](#5-volumes-vs-bind-mounts--comparison)
- [6. Quick Command Reference](#6-quick-command-reference)
- [7. Best Practices](#7-best-practices)
- [8. Summary](#8-summary)

---

## 1. Introduction to Docker Storage

By default, Docker containers use **ephemeral storage** — all data written inside a container is lost permanently when the container is deleted. This behaviour is by design for stateless workloads, but many real-world applications (databases, web servers, logs) require data to persist beyond the container lifecycle.

Docker provides two primary mechanisms to solve this problem:

- **Volumes** — Docker-managed storage located on the host file system, abstracted away from the container.
- **Bind Mounts** — Direct mapping of a specific host directory into the container.

> Understanding when and how to use each option is essential for building reliable, production-grade containerised applications.

---

## 2. Docker Volumes

Docker Volumes are the **recommended way to persist data**. They are fully managed by Docker and stored in a dedicated location on the host machine:

```
/var/lib/docker/volumes/<volume_name>/_data
```

Volumes offer several advantages over bind mounts including easier backup, migration, and sharing between multiple containers.

---

### 2.1 Volume Types

#### 📦 Named Volumes

Named volumes are explicitly created and assigned a user-defined name. They persist across container lifecycles and can be shared between multiple containers simultaneously.

```bash
# Create a named volume
docker volume create mydata

# Data is stored at:
/var/lib/docker/volumes/mydata/_data
```

#### 🔀 Anonymous Volumes

Anonymous volumes are automatically created by Docker when a container is run with a volume mount but no name is specified. Docker assigns a random hash as the name. These volumes are typically removed when the container is deleted.

```bash
# Anonymous volume — Docker assigns a random name
docker run -d --name mynginx2 -p 8080:80 \
  -v /usr/share/nginx/html nginx:1.28
```

> ⚠️ **Note:** Anonymous volumes are useful for temporary scratch space but are **not recommended** for data that needs to be retained.

---

### 2.2 Volume Management Commands

| Command | Description |
|---|---|
| `docker volume ls` | List all existing volumes on the host |
| `docker volume create mydata` | Create a new named volume called `mydata` |
| `docker volume rm mydata` | Delete a volume by name (must not be in use) |
| `docker volume inspect mydata` | Display detailed metadata about a volume |
| `docker volume prune` | Remove all unused (dangling) volumes |

---

### 2.3 Mounting Named Volumes to Containers

Use the `-v` flag when running a container to attach a volume. The format is:

```bash
docker run -v <volume_name>:<container_path> <image>
```

**Example — running two Nginx containers sharing the same named volume:**

```bash
# Container 1 — serves on port 80
docker run -d --name mynginx \
  -p 80:80 \
  -v mydata:/usr/share/nginx/html \
  nginx:1.28

# Container 2 — serves on port 8888 (shares same data)
docker run -d --name mynginx3 \
  -p 8888:80 \
  -v mydata:/usr/share/nginx/html \
  nginx:1.28
```

> ℹ️ Both containers mount the same `mydata` volume, so they serve identical content from `/usr/share/nginx/html`.

---

## 3. Bind Mounts

A **Bind Mount** maps a specific directory from the host machine directly into the container. Unlike volumes, bind mounts are **not managed by Docker** — the user is fully responsible for the host directory path.

This makes bind mounts ideal for development workflows where you want live changes on the host to be immediately reflected inside the container.

---

### 3.1 Syntax

```bash
docker run -v <host_directory>:<container_path> <image>
```

---

### 3.2 Example — Nginx with Bind Mount

```bash
# Mount a host directory as Nginx web root
docker run -d \
  -p 80:80 \
  -v /home/ec2-user/shared-data:/usr/share/nginx/html \
  nginx:1.28
```

Any files placed in `/home/ec2-user/shared-data` on the host will be immediately accessible from inside the container at `/usr/share/nginx/html`.

---

### 3.3 Use Cases for Bind Mounts

- **Development environments** — edit source code on the host and see changes instantly in the container.
- **Configuration injection** — mount config files (e.g., `nginx.conf`) from the host without rebuilding the image.
- **Log collection** — write logs to a host directory for centralised monitoring.
- **Debugging & testing** — share data between host and container during development.

---

## 4. Read-Only Volumes

Both named volumes and bind mounts can be made **read-only** by appending the `:ro` flag. This prevents the container from writing back to the volume or host directory — useful for protecting sensitive configuration data or serving static assets.

### Syntax

```bash
docker run -v <source>:<container_path>:ro <image>
```

### Example

```bash
# Mount named volume as read-only
docker run -d \
  -p 80:80 \
  -v mydata:/usr/share/nginx/html:ro \
  nginx:1.28
```

> ⚠️ With `:ro`, the container can **read** files from the volume but **cannot** modify, create, or delete them. Any write attempt will result in a `Read-only file system` error.

---

## 5. Volumes vs Bind Mounts — Comparison

| Feature | Named Volume | Anonymous Volume | Bind Mount |
|---|---|---|---|
| **Name** | User-defined (e.g., `mydata`) | Auto-generated (random hash) | N/A (host path) |
| **Managed By** | Docker | Docker | User / Host OS |
| **Storage Location** | `/var/lib/docker/volumes/` | `/var/lib/docker/volumes/` | Any host directory |
| **Persistence** | ✅ Survives container delete | ❌ Removed with container | ✅ Host file system |
| **Portability** | 🟢 High — easy to share | 🔴 Low | 🟡 Medium |
| **Read-only Support** | ✅ Yes (`:ro` flag) | ✅ Yes (`:ro` flag) | ✅ Yes (`:ro` flag) |
| **Best For** | Databases, shared data | Temporary scratch space | Dev environments, configs |

---

## 6. Quick Command Reference

### Volume Lifecycle

| Command | Description |
|---|---|
| `docker volume create <name>` | Create a new named volume |
| `docker volume ls` | List all volumes |
| `docker volume inspect <name>` | Inspect volume metadata and mount point |
| `docker volume rm <name>` | Remove a specific volume |
| `docker volume prune` | Remove all unused volumes |

### Running Containers with Storage

| Command | Description |
|---|---|
| `docker run -v mydata:/path` | Attach named volume to container |
| `docker run -v /host/path:/path` | Attach bind mount to container |
| `docker run -v /path` | Create anonymous volume at `/path` |
| `docker run -v mydata:/path:ro` | Mount volume as read-only |

---

## 7. Best Practices

- ✅ **Prefer named volumes** over anonymous volumes in production — they are easier to manage, back up, and share.
- ✅ **Use bind mounts for development** to enable live code reloading without rebuilding images.
- ✅ **Apply `:ro`** wherever containers should not modify data — reduces the risk of accidental data corruption.
- ✅ **Run `docker volume prune`** periodically to clean up dangling volumes and free disk space.
- ✅ **Back up volume data** using a temporary container to tar the volume contents before deletion.
- ✅ **Use Docker Compose** for multi-container setups to declaratively define and share volumes across services.
- ❌ **Never store secrets** (passwords, API keys) directly in volumes without encryption or Docker Secrets management.

---

## 8. Summary

Docker provides flexible and powerful storage options suited to different use cases:

| Storage Type | When to Use |
|---|---|
| **Named Volume** | Production data, databases, shared state between containers |
| **Anonymous Volume** | Temporary data, throwaway containers |
| **Bind Mount** | Local development, config injection, log collection |
| **`:ro` flag** | Any scenario where container should not write back to storage |

Mastering Docker storage ensures your containerised applications are **stateful**, **resilient**, and **maintainable**.

---

> 📄 *Reference source: Docker official documentation & internal notes*  
> 🔗 For more: [docs.docker.com/storage](https://docs.docker.com/storage/)
