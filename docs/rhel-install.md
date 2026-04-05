# 🐧 Docker Installation — Linux (RHEL)

Detailed guide for installing Docker Engine on Red Hat Enterprise Linux (RHEL) 8.x and 9.x.

---

## System Requirements

| Requirement | Details |
|-------------|---------|
| OS | RHEL 8.x or 9.x |
| Architecture | x86_64 / amd64 |
| Access | Root or `sudo` privileges |
| Network | Internet access required |
| Disk Space | ~500 MB for Docker Engine |

---

## Quick Install (Automated Script)

For a hands-off installation, use the provided script:

```bash
chmod +x scripts/install-docker-rhel.sh
sudo ./scripts/install-docker-rhel.sh
```

---

## Manual Installation

### Pre-step: Update the System

Always update packages before a major installation:

```bash
sudo dnf update -y
```

---

### Step 1 — Remove Conflicting Packages

RHEL ships with **Podman** and **Buildah** by default. These conflict with Docker's packages and must be removed first.

```bash
sudo dnf remove -y podman buildah runc
```

> This will not remove your existing containers or images — only the CLI tools.

---

### Step 2 — Install Required Dependencies

Install the `dnf-plugins-core` package, which provides the `config-manager` subcommand:

```bash
sudo dnf -y install dnf-plugins-core
```

---

### Step 3 — Add the Docker Repository

Add Docker's official RHEL repository:

```bash
sudo dnf config-manager \
    --add-repo \
    https://download.docker.com/linux/rhel/docker-ce.repo
```

Verify the repo was added:

```bash
dnf repolist | grep docker
```

---

### Step 4 — Install Docker Engine

Install Docker Engine, the CLI, and containerd:

```bash
sudo dnf install -y docker
```

To install a specific version:

```bash
# List available versions
dnf list docker-ce --showduplicates | sort -r

# Install a specific version (example)
sudo dnf install -y docker-ce-26.1.4
```

---

### Step 5 — Start and Enable Docker

Start the Docker daemon and configure it to start automatically on boot:

```bash
sudo systemctl enable --now docker
```

Verify the service is running:

```bash
sudo systemctl status docker
```

You should see:

```
● docker.service - Docker Application Container Engine
     Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled)
     Active: active (running)
```

---

### Step 6 — Verify Installation

Run the `hello-world` container:

```bash
sudo docker run hello-world
```

---

## Post-Installation

### Run Docker Without `sudo`

```bash
# Add your user to the docker group
sudo usermod -aG docker $USER

# Apply the change (or log out and back in)
newgrp docker

# Verify — should work without sudo
docker run hello-world
```

### Configure Docker to Use a Proxy (if needed)

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d

sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf <<EOF
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:3128"
Environment="HTTPS_PROXY=http://proxy.example.com:3128"
Environment="NO_PROXY=localhost,127.0.0.1"
EOF

sudo systemctl daemon-reload
sudo systemctl restart docker
```

### Manage Docker as a Service

```bash
sudo systemctl start docker      # Start
sudo systemctl stop docker       # Stop
sudo systemctl restart docker    # Restart
sudo systemctl status docker     # Status
sudo systemctl disable docker    # Disable autostart
```

---

## Uninstalling Docker

```bash
# Stop the service
sudo systemctl stop docker

# Remove packages
sudo dnf remove -y docker docker-ce docker-ce-cli containerd.io

# Remove data (images, containers, volumes) — IRREVERSIBLE
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```
