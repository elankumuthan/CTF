#!/bin/bash

cd /home/dockUbuntu/CTF || {
    echo "[-] Failed to access /home/ubuntu/CTF"
    exit 1
}

echo "[~] Stopping Docker Compose containers..."
docker compose down --volumes --remove-orphans

echo "[~] Pruning unused Docker resources..."
docker system prune -af --volumes

echo "[+] All Docker containers, images, and volumes have been cleaned up."
