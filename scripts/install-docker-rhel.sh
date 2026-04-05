#!/usr/bin/env bash
# =============================================================================
# install-docker-rhel.sh
# Automated Docker Engine installation for RHEL 8.x / 9.x
#
# Usage:
#   chmod +x install-docker-rhel.sh
#   sudo ./install-docker-rhel.sh
#
# Optional flags:
#   --no-sudo-group   Skip adding the current user to the docker group
# =============================================================================

set -euo pipefail

# ── Colour helpers ────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; NC='\033[0m'

info()    { echo -e "${CYAN}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

# ── Parse flags ───────────────────────────────────────────────────────────────
ADD_TO_GROUP=true
for arg in "$@"; do
  [[ "$arg" == "--no-sudo-group" ]] && ADD_TO_GROUP=false
done

# ── Root check ────────────────────────────────────────────────────────────────
[[ "$EUID" -ne 0 ]] && error "Please run as root or with sudo."

# ── OS check ─────────────────────────────────────────────────────────────────
if ! grep -qiE "rhel|red hat" /etc/os-release 2>/dev/null; then
  warn "This script is designed for RHEL. Proceed with caution on other distros."
fi

echo ""
echo "============================================="
echo "   Docker Engine Installer — RHEL 8/9"
echo "============================================="
echo ""

# ── Step 1: System update ─────────────────────────────────────────────────────
info "Updating system packages..."
dnf update -y
success "System updated."

# ── Step 2: Remove conflicting packages ──────────────────────────────────────
info "Removing conflicting container tools (podman, buildah, runc)..."
dnf remove -y podman buildah runc 2>/dev/null || true
success "Conflicting packages removed (or were not installed)."

# ── Step 3: Install dependencies ─────────────────────────────────────────────
info "Installing dnf-plugins-core..."
dnf -y install dnf-plugins-core
success "Dependencies installed."

# ── Step 4: Add Docker repository ────────────────────────────────────────────
info "Adding Docker repository..."
dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
success "Docker repository added."

# ── Step 5: Install Docker Engine ────────────────────────────────────────────
info "Installing Docker Engine..."
dnf install -y docker
success "Docker Engine installed."

# ── Step 6: Start and enable Docker ──────────────────────────────────────────
info "Starting and enabling Docker service..."
systemctl enable --now docker
success "Docker service started and enabled."

# ── Step 7: Add user to docker group (optional) ───────────────────────────────
if [[ "$ADD_TO_GROUP" == true && -n "${SUDO_USER:-}" ]]; then
  info "Adding '${SUDO_USER}' to the docker group..."
  usermod -aG docker "$SUDO_USER"
  success "User '${SUDO_USER}' added to docker group. Log out and back in to apply."
fi

# ── Step 8: Verify installation ───────────────────────────────────────────────
info "Verifying Docker installation..."
docker_version=$(docker --version)
success "Docker installed: ${docker_version}"

echo ""
echo "============================================="
echo -e "  ${GREEN}Docker installation complete!${NC}"
echo "============================================="
echo ""
echo "  Run the following to test:"
echo "    sudo docker run hello-world"
echo ""
if [[ "$ADD_TO_GROUP" == true && -n "${SUDO_USER:-}" ]]; then
  echo "  After re-login, run without sudo:"
  echo "    docker run hello-world"
  echo ""
fi
