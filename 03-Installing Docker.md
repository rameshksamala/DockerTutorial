# 🐳 Installing Docker

> A step-by-step guide to installing Docker on **Windows** and **Linux (RHEL)**.


---

## 📋 Table of Contents

- [Overview](#overview)
- [Windows Installation](#-windows-installation)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
  - [Verify Installation](#verify-installation)
- [Linux (RHEL) Installation](#-linux-rhel-installation)
  - [Prerequisites](#prerequisites-1)
  - [Step-by-Step Guide](#step-by-step-guide)
  - [Optional: Run Docker Without sudo](#optional-run-docker-without-sudo)
- [Quick-Start Scripts](#-quick-start-scripts)
- [Troubleshooting](#-troubleshooting)
- [Further Reading](#-further-reading)


---

## Overview

Docker is an open-source containerization platform. This guide covers installation on two of the most common environments:

| Platform | Method |
|----------|--------|
| 🪟 Windows 10 / 11 | Docker Desktop (GUI installer) |
| 🐧 Linux — RHEL 8.x / 9.x | Docker Engine via `dnf` package manager |

---

## 🪟 Windows Installation

### Prerequisites

Before installing, make sure your system meets these requirements:

| Requirement | Details |
|-------------|---------|
| OS | Windows 10 or 11 (64-bit) |
| WSL 2 | Must be enabled |
| Virtualization | Must be enabled in BIOS |

> **Need help enabling WSL 2?** Run this in PowerShell as Administrator:
> ```powershell
> wsl --install
> ```

### Installation Steps

**1. Download Docker Desktop**

Go to [docker.com](https://www.docker.com/products/docker-desktop/) and download **Docker Desktop for Windows**.

**2. Run the Installer**

Double-click `Docker Desktop Installer.exe` and follow the setup wizard.

**3. Enable WSL 2 Backend (Recommended)**

During installation, check **"Use WSL 2 instead of Hyper-V"** if prompted.

**4. Restart Your Machine**

A full restart is required to apply the changes.

**5. Launch Docker Desktop**

Open Docker Desktop from the Start menu. Wait for the Docker engine to start — you'll see the **whale icon** appear in the taskbar.

### Verify Installation

Open a terminal (PowerShell or Command Prompt) and run:

```powershell
docker --version
```

Then test with the hello-world container:

```powershell
docker run hello-world
```

Expected output:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## 🐧 Linux (RHEL) Installation

### Prerequisites

| Requirement | Details |
|-------------|---------|
| OS | RHEL 8.x or 9.x (x86_64 / amd64) |
| Access | Root or `sudo` access |
| Network | Internet access to fetch Docker packages |

> **📝 Note:** Update your system first before installing:
> ```bash
> sudo dnf update -y
> ```

### Step-by-Step Guide

#### Step 1 — Remove Conflicting Packages

Podman, Buildah, and other container tools can conflict with Docker. Remove them first:

```bash
sudo dnf remove -y podman buildah runc
```

#### Step 2 — Install Required Dependencies

```bash
sudo dnf -y install dnf-plugins-core
```

#### Step 3 — Set Up the Docker Repository

```bash
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
```

#### Step 4 — Install Docker Engine

```bash
sudo dnf install -y docker
```

#### Step 5 — Start and Enable the Docker Service

```bash
sudo systemctl enable --now docker
```

Check that Docker is running:

```bash
sudo systemctl status docker
```

You should see `active (running)` in the output.

#### Step 6 — Verify Installation

Run the hello-world container to confirm everything works:

```bash
sudo docker run hello-world
```

### Optional: Run Docker Without `sudo`

By default, Docker requires `sudo`. To run Docker commands as your regular user, add yourself to the `docker` group:

```bash
sudo usermod -aG docker $USER
```

> **📝 Note:** Log out and back in for this change to take effect. You can verify with:
> ```bash
> docker run hello-world
> ```

---

## ⚡ Quick-Start Scripts

Automated shell scripts are available in the [`scripts/`](./scripts/) directory:

| Script | Description |
|--------|-------------|
| [`install-docker-rhel.sh`](scripts/install-docker-rhel.sh) | Full automated install for RHEL 8/9 |

> **Windows users:** Use the [official Docker Desktop installer](https://www.docker.com/products/docker-desktop/) — no script needed.

---

## 🔧 Troubleshooting

### Windows

| Issue | Fix |
|-------|-----|
| Docker Desktop won't start | Ensure WSL 2 is installed: `wsl --install` |
| Virtualization error | Enable virtualization in BIOS/UEFI settings |
| WSL 2 kernel missing | Run `wsl --update` in PowerShell |

### Linux (RHEL)

| Issue | Fix |
|-------|-----|
| `Cannot connect to Docker daemon` | Run `sudo systemctl start docker` |
| `Permission denied` | Add user to docker group: `sudo usermod -aG docker $USER` then re-login |
| Package conflicts | Remove conflicting tools: `sudo dnf remove -y podman buildah runc` |
| Repo not found | Re-add the Docker repo (Step 3) |

---

## 📚 Further Reading

- [Docker Official Documentation](https://docs.docker.com/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Docker Engine on RHEL](https://docs.docker.com/engine/install/rhel/)
- [WSL 2 Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/)

---


