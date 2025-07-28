#!/bin/bash
set -e

cd /home/dockUbuntu/CTF || {
    echo "[-] Failed to access /home/dockUbuntu/CTF"
    exit 1
}

echo "[~] Starting Docker Compose..."
docker compose up --build -d

echo "[~] Waiting for containers to be ready..."
# Wait for containers to be fully up and running
sleep 5

# Check if containers are actually running
if docker compose ps --services --filter "status=running" | grep -q .; then
    echo "[+] Docker Compose containers are running successfully."
else
    echo "[-] Docker Compose containers failed to start properly."
    docker compose logs
    exit 1
fi

echo "[~] Starting Docker hardening script..."
if [ -f "docker_hardening/harden_docker.sh" ]; then
    chmod +x docker_hardening/harden_docker.sh
    docker_hardening/harden_docker.sh
    echo "[+] Docker hardening completed successfully."
else
    echo "[-] Docker hardening script not found at docker_hardening/harden_docker.sh"
    exit 1
fi

echo "[+] Setup complete! Docker Compose is running with hardening applied."
