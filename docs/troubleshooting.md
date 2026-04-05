# 🔧 Troubleshooting Docker Installation

Common issues and fixes for Docker installation on Windows and RHEL.

---

## 🪟 Windows

### Docker Desktop Won't Start

**Symptom:** Docker Desktop opens but the engine never starts, or closes immediately.

**Fixes:**
1. Ensure WSL 2 is installed and up to date:
   ```powershell
   wsl --install
   wsl --update
   ```
2. Restart your machine fully (not sleep/hibernate).
3. Check Windows Event Viewer for errors under `Application and Services Logs → Docker Desktop`.

---

### "Hardware Assisted Virtualization Is Not Enabled"

**Symptom:** Error on launch about virtualization not being available.

**Fix:** Enable virtualization in BIOS:
- Intel: Enable **VT-x**
- AMD: Enable **AMD-V / SVM**

Restart your machine and enter BIOS (usually `Del`, `F2`, or `F10` on boot).

---

### WSL 2 Kernel Update Required

**Symptom:** Prompt saying WSL 2 kernel must be updated before Docker Desktop can start.

**Fix:**
```powershell
wsl --update
wsl --shutdown
```
Then restart Docker Desktop.

---

### `docker: command not found` in Terminal

**Symptom:** Running `docker` in PowerShell or CMD returns an error.

**Fix:**
- Make sure Docker Desktop is running (whale icon in taskbar)
- Restart the terminal after Docker Desktop has fully started

---

## 🐧 Linux (RHEL)

### Cannot Connect to the Docker Daemon

**Symptom:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Fix:**
```bash
# Start Docker
sudo systemctl start docker

# Confirm it's running
sudo systemctl status docker
```

---

### Permission Denied (Running Without sudo)

**Symptom:**
```
Got permission denied while trying to connect to the Docker daemon socket
```

**Fix:**
```bash
sudo usermod -aG docker $USER
newgrp docker   # Apply immediately, or log out and back in
```

---

### Package Conflicts on Install

**Symptom:** `dnf install docker` fails due to conflicts with podman, runc, etc.

**Fix:**
```bash
sudo dnf remove -y podman buildah runc
sudo dnf install -y docker
```

---

### Repository Not Found / GPG Key Error

**Symptom:** `dnf` cannot find the Docker package or GPG validation fails.

**Fix:** Re-add the Docker repository:
```bash
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
sudo dnf makecache
sudo dnf install -y docker
```

---

### Docker Fails to Start After Install

**Symptom:** `systemctl status docker` shows `failed` or `inactive`.

**Fix:**
```bash
# Check detailed logs
sudo journalctl -u docker -n 50 --no-pager

# Common causes:
# - Conflicting runc version → reinstall
sudo dnf reinstall -y runc
sudo systemctl start docker
```

---

### `hello-world` Container Fails to Pull

**Symptom:** `docker run hello-world` shows a network timeout or pull error.

**Fix — Check internet access:**
```bash
curl -I https://registry-1.docker.io
```

**Fix — Configure a proxy** (if behind a corporate firewall):
```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf <<EOF
[Service]
Environment="HTTP_PROXY=http://your-proxy:3128"
Environment="HTTPS_PROXY=http://your-proxy:3128"
EOF
sudo systemctl daemon-reload && sudo systemctl restart docker
```

---

## Getting Further Help

- [Docker Community Forums](https://forums.docker.com/)
- [Docker GitHub Issues](https://github.com/docker/docker-ce/issues)
- [Stack Overflow — docker tag](https://stackoverflow.com/questions/tagged/docker)
