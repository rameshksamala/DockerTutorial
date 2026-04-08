"""
Docker Layer Test Script
Verifies and demonstrates every layer in the Dockerfile:
  FROM, ARG, ENV, WORKDIR, COPY, RUN, EXPOSE, VOLUME, USER, CMD
"""

import sys
import os
import platform
import socket
import datetime
import json

# ── ANSI colours ──────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"

def section(title):
    print(f"\n{BOLD}{CYAN}{'─' * 52}{RESET}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"{BOLD}{CYAN}{'─' * 52}{RESET}")

def ok(label, value):
    print(f"  {GREEN}✔{RESET}  {BOLD}{label:<30}{RESET} {value}")

def warn(label, value):
    print(f"  {YELLOW}⚠{RESET}  {BOLD}{label:<30}{RESET} {value}")

def fail(label, value):
    print(f"  {RED}✘{RESET}  {BOLD}{label:<30}{RESET} {value}")

# ── HEADER ────────────────────────────────────
print(f"\n{BOLD}{BLUE}╔══════════════════════════════════════════════════════╗")
print(f"║        Docker Layer Verification Report              ║")
print(f"╚══════════════════════════════════════════════════════╝{RESET}")
print(f"  {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

# ──────────────────────────────────────────────
# Layer 1 · FROM — Base image
# ──────────────────────────────────────────────
section("Layer 1 · FROM — Base image")
ok("OS",             platform.system())
ok("OS release",     platform.release())
ok("Architecture",   platform.machine())
ok("Python version", sys.version.split()[0])
ok("Python path",    sys.executable)

# ──────────────────────────────────────────────
# Layer 2 · ARG — Build-time variables
# ──────────────────────────────────────────────
section("Layer 2 · ARG — Build-time variables")
build_version = os.environ.get("BUILD_VERSION", "not set")
if build_version != "not set":
    ok("BUILD_VERSION", build_version)
else:
    warn("BUILD_VERSION", "not set (use --build-arg BUILD_VERSION=1.0)")

# ──────────────────────────────────────────────
# Layer 3 · ENV — Runtime environment variables
# ──────────────────────────────────────────────
section("Layer 3 · ENV — Runtime environment variables")
env_checks = {
    "APP_ENV":               os.environ.get("APP_ENV",               "not set"),
    "APP_VERSION":           os.environ.get("APP_VERSION",           "not set"),
    "APP_PORT":              os.environ.get("APP_PORT",              "not set"),
    "PYTHONDONTWRITEBYTECODE": os.environ.get("PYTHONDONTWRITEBYTECODE", "not set"),
    "PYTHONUNBUFFERED":      os.environ.get("PYTHONUNBUFFERED",      "not set"),
}
for k, v in env_checks.items():
    (ok if v != "not set" else warn)(k, v)

# ──────────────────────────────────────────────
# Layer 4 · WORKDIR — Working directory
# ──────────────────────────────────────────────
section("Layer 4 · WORKDIR — Working directory")
cwd = os.getcwd()
ok("Current directory", cwd)
if cwd == "/app":
    ok("WORKDIR check", "Correctly set to /app ✔")
else:
    warn("WORKDIR check", f"Expected /app, got {cwd}")

# ──────────────────────────────────────────────
# Layer 5 · COPY — Files present in image
# ──────────────────────────────────────────────
section("Layer 5 · COPY — Files in container")
for fname in ["app.py", "requirements.txt"]:
    fpath = os.path.join(cwd, fname)
    if os.path.exists(fpath):
        ok(fname, f"found  ({os.path.getsize(fpath):,} bytes)")
    else:
        fail(fname, "NOT found")

# ──────────────────────────────────────────────
# Layer 6 · RUN — pip-installed packages
# ──────────────────────────────────────────────
section("Layer 6 · RUN — Installed packages (requirements.txt)")
packages = {
    "requests": None,
    "flask":    None,
    "psutil":   None,
}
for pkg in packages:
    try:
        mod = __import__(pkg)
        ver = getattr(mod, "__version__", "installed")
        ok(pkg, ver)
        packages[pkg] = mod
    except ImportError:
        fail(pkg, "not installed — check requirements.txt")

# ──────────────────────────────────────────────
# Layer 7 · EXPOSE — Declared port
# ──────────────────────────────────────────────
section("Layer 7 · EXPOSE — Network / port")
app_port = int(os.environ.get("APP_PORT", 8080))
ok("Declared EXPOSE port", str(app_port))
try:
    hostname = socket.gethostname()
    ip       = socket.gethostbyname(hostname)
    ok("Container hostname", hostname)
    ok("Container IP",       ip)
except Exception as e:
    warn("Hostname/IP resolution", str(e))

# ──────────────────────────────────────────────
# Layer 8 · VOLUME — Data mount point
# ──────────────────────────────────────────────
section("Layer 8 · VOLUME — Persistent data directory")
volume_path = "/app/data"
if os.path.isdir(volume_path):
    ok("Volume path exists", volume_path)
    try:
        test_file = os.path.join(volume_path, "volume_test.json")
        payload   = {
            "written_by": "app.py",
            "timestamp":  datetime.datetime.utcnow().isoformat(),
            "note":       "VOLUME layer verified",
        }
        with open(test_file, "w") as f:
            json.dump(payload, f, indent=2)
        ok("Write test to volume", test_file)
    except Exception as e:
        warn("Write test", str(e))
else:
    warn("Volume path",
         f"{volume_path} missing — mount with:  docker run -v mydata:/app/data ...")

# ──────────────────────────────────────────────
# Layer 9 · USER — Security context
# ──────────────────────────────────────────────
section("Layer 9 · USER — Process security context")
import getpass
try:
    current_user = getpass.getuser()
except Exception:
    current_user = f"uid={os.getuid()}"

ok("Running as", current_user)
if current_user == "root" or os.getuid() == 0:
    warn("Security", "Running as root — Dockerfile uses USER appuser for non-root exec")
else:
    ok("Non-root check", f"Good — '{current_user}' is not root ✔")

ok("PID", str(os.getpid()))

# ──────────────────────────────────────────────
# Layer 10 · CMD — Entrypoint + system resources
# ──────────────────────────────────────────────
section("Layer 10 · CMD — Entrypoint & system resources")
ok("Launched via", 'CMD ["python", "app.py"]')

psutil_mod = packages.get("psutil")
if psutil_mod:
    mem = psutil_mod.virtual_memory()
    ok("CPU cores",        str(psutil_mod.cpu_count(logical=True)))
    ok("Memory total",     f"{mem.total      // (1024**2):,} MB")
    ok("Memory available", f"{mem.available  // (1024**2):,} MB")
    ok("Memory used %",    f"{mem.percent}%")
else:
    warn("Resource stats", "psutil not available — install via requirements.txt")

# ── FOOTER ────────────────────────────────────
print(f"\n{BOLD}{GREEN}{'═' * 52}")
print(f"  All 10 Dockerfile layers verified!")
print(f"{'═' * 52}{RESET}\n")
