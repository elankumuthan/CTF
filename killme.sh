#!/bin/bash
set -e

cd /home/dockUbuntu/CTF || {
    echo "[-] Failed to access /home/dockUbuntu/CTF"
    exit 1
}

echo "[~] Stopping Docker Compose containers..."
docker compose down --volumes --remove-orphans

echo "[~] Pruning unused Docker resources..."
docker system prune -af --volumes

echo "[+] All Docker containers, images, and volumes have been cleaned up."

# Optional: Also clean up any remaining Docker networks
echo "[~] Cleaning up unused Docker networks..."
docker network prune -f

echo "[+] Complete cleanup finished. System is ready for fresh deployment."