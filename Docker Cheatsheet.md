# 🐳 Docker Cheatsheet

> Essential Docker commands — installation, image & container management

![Shell](https://img.shields.io/badge/Shell-script-green) ![Docker](https://img.shields.io/badge/Docker-cheatsheet-blue)

---

## Installation & Setup

```bash
docker --version

sudo dnf install docker -y

sudo systemctl enable docker --now

sudo systemctl status docker

sudo usermod -aG docker $USER        # run docker without sudo
```

---

## Images

| Command | Description |
|---------|-------------|
| `docker images` | List local images |
| `docker docker history <image>` | Show all layers and their sizes |
| `docker inspect <image>` | Show full image metadata in JSON |
| `docker pull <image>` | Download image from registry |
| `docker push <image>` | Upload image to registry |
| `docker rmi <image>` | Remove a local image |
| `docker system prune` | Remove all unused images, containers, networks |
| `docker build --no-cache` | Force full rebuild, ignoring cache |
| `docker build -t name:tag ` | Build image from Dockerfile in current directory |

---

## Container Lifecycle

| Command | Description |
|---------|-------------|
| `docker ps` | List running containers |
| `docker ps -a` | List all containers (running + exited) |
| `docker run nginx:1.28` | Run nginx 1.28 in foreground |
| `docker run -d nginx:1.28` | Run nginx 1.28 in detached mode |
| `docker run -d --name my-web nginx:1.28` | Detached with custom name |
| `docker run --rm --name test-delete nginx` | Auto-remove container on stop |

---

## Start / Stop / Kill

| Command | Description |
|---------|-------------|
| `docker stop <id/name>` | Graceful shutdown (SIGTERM) |
| `docker start <id/name>` | Start a stopped container |
| `docker kill <id/name>` | Immediate shutdown (SIGKILL) |
| `docker rm <id/name>` | Remove a container |

> **stop vs kill:** `stop` sends SIGTERM (graceful, allows cleanup), `kill` sends SIGKILL (immediate, no cleanup).

---

## 🔍 Inspect & Logs

| Command | Description |
|---------|-------------|
| `docker logs <id/name>` | Show container logs |
| `docker logs -f <id/name>` | Follow (tail) live logs |
| `docker inspect <id/name>` | Detailed JSON info about container/image |
| `docker stats` | Live CPU/memory usage of running containers |
| `docker top <id/name>` | Running processes inside container |

---

## 🔌 Exec & Shell Access

| Command | Description |
|---------|-------------|
| `docker exec -it <id/name> bash` | Open interactive bash shell |
| `docker exec -it <id/name> sh` | Open sh (for alpine-based images) |
| `docker exec <id/name> <cmd>` | Run a one-off command inside container |

> **`-it`** = interactive + TTY. Required for shell sessions.

---

## 🌐 Port Mapping

| Command | Description |
|---------|-------------|
| `docker run -p 8080:80 nginx` | Map host port 8080 → container port 80 |
| `docker run -p 127.0.0.1:8080:80 nginx` | Bind to localhost only |
| `docker port <id/name>` | Show port mappings for a container |

---

## 📂 Volumes & Bind Mounts

| Command | Description |
|---------|-------------|
| `docker volume create mydata` | Create a named volume |
| `docker volume ls` | List volumes |
| `docker volume rm mydata` | Remove a volume |
| `docker run -v mydata:/app/data nginx` | Mount named volume into container |
| `docker run -v $(pwd):/app nginx` | Bind mount current directory |

---

## 🏗️ Build Images

| Command | Description |
|---------|-------------|
| `docker build -t myapp:1.0 .` | Build image from Dockerfile in current dir |
| `docker build -f Dockerfile.dev .` | Use a specific Dockerfile |
| `docker tag myapp:1.0 myapp:latest` | Tag an image |
| `docker rmi <image-id>` | Remove an image |
| `docker image prune` | Remove dangling (untagged) images |

---

## 📦 Registry & Push/Pull

| Command | Description |
|---------|-------------|
| `docker pull nginx:latest` | Pull image from Docker Hub |
| `docker push myuser/myapp:1.0` | Push image to Docker Hub |
| `docker login` | Authenticate with Docker Hub |
| `docker logout` | Log out |

---

## 🌍 Networking

| Command | Description |
|---------|-------------|
| `docker network ls` | List networks |
| `docker network create mynet` | Create a custom bridge network |
| `docker network inspect mynet` | Inspect a network |
| `docker run --network mynet nginx` | Run container on a specific network |
| `docker network rm mynet` | Remove a network |

---

## 🧹 Cleanup

| Command | Description |
|---------|-------------|
| `docker rm $(docker ps -aq)` | Remove all stopped containers |
| `docker rmi $(docker images -q)` | Remove all images |
| `docker system prune` | Remove stopped containers, unused networks, dangling images |
| `docker system prune -a` | Full cleanup including unused images |
| `docker volume prune` | Remove unused volumes |

> **Caution:** `system prune -a` removes all unused images, not just dangling ones.
