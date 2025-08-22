#!/bin/bash
set -e

cd /home/dockUbuntu/CTF || {
    echo "[-] Failed to access /home/dockUbuntu/CTF"
    exit 1
}

echo "[~] Docker Compose containers..."
docker compose down --volumes --remove-orphans

echo "[~] Removing Docker hardening..."
if [ -f "docker_hardening/unharden_docker.sh" ]; then
    chmod +x docker_hardening/unharden_docker.sh
    docker_hardening/unharden_docker.sh
    echo "[+] Removing docker hardening completed successfully."
else
    echo "[-] Docker unhardening script not found at docker_hardening/unharden_docker.sh"
    exit 1
fi

echo "[+] Complete cleanup finished. System is ready for fresh deployment."
