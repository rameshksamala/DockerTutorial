# 🐳 Docker Management — Command Reference

> A comprehensive reference guide for essential Docker commands with syntax, explanations, and examples.

---

## 📋 Table of Contents

1. [docker --version](#1-docker---version)
2. [docker login](#2-docker-login)
3. [docker search](#3-docker-search)
4. [docker pull](#4-docker-pull)
5. [docker inspect](#5-docker-inspect)
6. [docker create](#6-docker-create)
7. [docker start](#7-docker-start)
8. [docker run](#8-docker-run)
9. [docker ps -a](#9-docker-ps--a)
10. [docker exec](#10-docker-exec)
11. [docker stop](#11-docker-stop)
12. [docker images](#12-docker-images)
13. [docker rm](#13-docker-rm)
14. [docker rmi](#14-docker-rmi)

---

## 1. `docker --version`

### 📝 Syntax

```bash
docker --version
docker version
```

### 💡 Explanation

Displays the installed version of the Docker client and (with `docker version`) also shows the server/daemon version, API version, and other details. Useful for checking compatibility or troubleshooting.

### ▶️ Example

```bash
docker --version
# Output: Docker version 27.0.3, build 7d4bcd8
```

---

## 2. `docker login`

### 📝 Syntax

```bash
docker login
docker login -u <username>
docker login <registry>   # e.g., docker login myregistry.com
```

### 💡 Explanation

Logs you into a Docker registry (default is Docker Hub). You will be prompted for username and password (or use `-u` and `-p` flags). Once logged in, you can push and pull private images. Credentials are stored locally.

### ▶️ Example

```bash
docker login
# Username: yourusername
# Password: ********
# Login Succeeded
```

---

## 3. `docker search`

### 📝 Syntax

```bash
docker search <image_name>
docker search <image_name> --filter "is-official=true"
```

### 💡 Explanation

Searches for Docker images on Docker Hub (or configured registry). Shows image name, description, stars, and official status.

### ▶️ Example

```bash
docker search nginx
```

---

## 4. `docker pull`

### 📝 Syntax

```bash
docker pull <image_name>
docker pull <image_name>:<tag>        # e.g., nginx:alpine
docker pull <registry>/<image_name>
```

### 💡 Explanation

Downloads a Docker image from a registry (default: Docker Hub) to your local machine.

### ▶️ Example

```bash
docker pull nginx:latest
```

---

## 5. `docker inspect`

### 📝 Syntax

```bash
docker inspect <container_id_or_name>
docker inspect <image_name>
docker inspect --format '{{.State.Status}}' <container_name>
```

### 💡 Explanation

Shows detailed low-level information about a container or image in JSON format (configuration, state, network settings, mounts, etc.). Very useful for debugging.

### ▶️ Example

```bash
docker inspect mycontainer
```

---

## 6. `docker create`

### 📝 Syntax

```bash
docker create [OPTIONS] <image_name> [COMMAND] [ARG...]
# Common options: --name, -e, -p, -v, --rm
```

### 💡 Explanation

Creates a new container from an image **without starting it**. You can later start it with `docker start`. It is the first step of the `docker run` process.

### ▶️ Example

```bash
docker create --name myweb -p 8080:80 nginx
```

---

## 7. `docker start`

### 📝 Syntax

```bash
docker start <container_id_or_name>
docker start -a <container_name>   # Attach to stdout/stderr
```

### 💡 Explanation

Starts one or more stopped containers.

### ▶️ Example

```bash
docker start myweb
```

---

## 8. `docker run`

### 📝 Syntax

```bash
docker run [OPTIONS] <image_name> [COMMAND] [ARG...]
```

| Option | Description |
|--------|-------------|
| `-d` / `--detach` | Run container in background |
| `-it` | Interactive mode + pseudo-TTY |
| `--name <name>` | Assign a name to the container |
| `-p <host>:<container>` | Map host port to container port |
| `-v <host>:<container>` | Mount a volume |
| `--rm` | Auto-remove container when stopped |

### 💡 Explanation

Creates **and** starts a new container from an image. This is the most commonly used command for running applications in containers.

### ▶️ Example

```bash
docker run -d --name mynginx -p 80:80 nginx
docker run -it ubuntu bash
```

---

## 9. `docker ps -a`

### 📝 Syntax

```bash
docker ps        # Running containers only
docker ps -a     # All containers (running + stopped)
docker ps -q     # Only container IDs
```

### 💡 Explanation

Lists containers. Without `-a` it shows only running containers. Very useful to check status, ports, and names.

### ▶️ Example

```bash
docker ps -a
```

---

## 10. `docker exec`

### 📝 Syntax

```bash
docker exec [OPTIONS] <container_name> <command>
docker exec -it <container_name> /bin/bash   # or sh
```

### 💡 Explanation

Executes a command inside a **running** container. Commonly used to open an interactive shell or run debugging commands.

### ▶️ Example

```bash
docker exec -it mynginx bash
```

---

## 11. `docker stop`

### 📝 Syntax

```bash
docker stop <container_id_or_name>
docker stop -t 10 <container_name>   # Set timeout in seconds
```

### 💡 Explanation

Gracefully stops a running container by sending `SIGTERM` (then `SIGKILL` after timeout).

### ▶️ Example

```bash
docker stop mynginx
```

---

## 12. `docker images`

### 📝 Syntax

```bash
docker images
docker image ls
docker images -a   # Show all images (including intermediate)
```

### 💡 Explanation

Lists all Docker images stored locally on your machine.

### ▶️ Example

```bash
docker images
```

---

## 13. `docker rm`

### 📝 Syntax

```bash
docker rm <container_id_or_name>
docker rm -f <container_name>       # Force remove (even if running)
docker rm $(docker ps -a -q)        # Remove all containers
```

### 💡 Explanation

Removes one or more **stopped** containers. Use `-f` to force-remove running containers.

### ▶️ Example

```bash
docker rm myoldcontainer
```

---

## 14. `docker rmi`

### 📝 Syntax

```bash
docker rmi <image_name_or_id>
docker rmi -f <image_id>      # Force remove
docker image prune            # Remove dangling images
```

### 💡 Explanation

Removes (deletes) one or more Docker images from your local storage.

### ▶️ Example

```bash
docker rmi nginx:alpine
```

---

## 🗂️ Quick Reference Summary

| # | Command | Description |
|---|---------|-------------|
| 1 | `docker --version` | Show Docker version info |
| 2 | `docker login` | Log in to a Docker registry |
| 3 | `docker search` | Search for images on Docker Hub |
| 4 | `docker pull` | Download an image from a registry |
| 5 | `docker inspect` | Show detailed info on container/image |
| 6 | `docker create` | Create a container without starting it |
| 7 | `docker start` | Start a stopped container |
| 8 | `docker run` | Create and start a container |
| 9 | `docker ps -a` | List all containers |
| 10 | `docker exec` | Run a command in a running container |
| 11 | `docker stop` | Gracefully stop a running container |
| 12 | `docker images` | List local images |
| 13 | `docker rm` | Remove stopped containers |
| 14 | `docker rmi` | Remove local images |

---

*Generated from Docker Management Command Reference*
