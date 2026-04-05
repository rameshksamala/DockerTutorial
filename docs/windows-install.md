# 🪟 Docker Installation — Windows

Detailed guide for installing Docker Desktop on Windows 10 / 11.

---

## System Requirements

| Requirement | Minimum |
|-------------|---------|
| OS | Windows 10 (21H2+) or Windows 11 (64-bit) |
| RAM | 4 GB minimum (8 GB recommended) |
| WSL 2 | Enabled |
| Virtualization | Enabled in BIOS/UEFI |
| Disk Space | 2 GB for Docker Desktop |

---

## Pre-Installation Checklist

### 1. Enable WSL 2

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

Then restart your machine. After restart, update the WSL kernel:

```powershell
wsl --update
wsl --set-default-version 2
```

### 2. Check Virtualization

Open **Task Manager → Performance → CPU**. Confirm **Virtualization: Enabled**.

If not enabled, restart and enter BIOS (usually `Del`, `F2`, or `F10` on boot) and enable **Intel VT-x** or **AMD-V**.

---

## Installation Steps

### Step 1 — Download Docker Desktop

Visit the official page: https://www.docker.com/products/docker-desktop/

Click **Download for Windows**.

### Step 2 — Run the Installer

1. Double-click `Docker Desktop Installer.exe`
2. Follow the setup wizard
3. When prompted, select **"Use WSL 2 instead of Hyper-V"** (recommended)
4. Click **OK** and wait for installation to complete

### Step 3 — Restart

Restart your machine when prompted.

### Step 4 — Launch Docker Desktop

Open **Docker Desktop** from the Start menu. The Docker engine starts automatically — wait for the **whale icon** in the system tray to become steady (not animated).

---

## Verify Installation

Open **PowerShell** or **Windows Terminal** and run:

```powershell
# Check Docker version
docker --version

# Run a test container
docker run hello-world
```

Expected output from `hello-world`:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Docker Desktop fails to start | WSL 2 not installed | Run `wsl --install` in PowerShell |
| "Hardware assisted virtualization" error | Virtualization disabled in BIOS | Enable VT-x / AMD-V in BIOS |
| WSL 2 kernel update required | Outdated WSL kernel | Run `wsl --update` |
| Docker is slow | Insufficient RAM | Allocate more RAM in Docker Desktop → Settings → Resources |

---

## Docker Desktop Settings (Recommended)

After installation, open **Docker Desktop → Settings**:

- **Resources → Memory**: Set to at least 4 GB
- **WSL Integration**: Enable for your default WSL distro
- **Start Docker Desktop when you log in**: Enable for convenience
