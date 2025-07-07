#!/bin/bash

cd /home/dockUbuntu/CTF || {
    echo "[-] Failed to access /home/ubuntu/CTF"
    exit 1
}

echo "[~] Starting Docker Compose..."
docker compose up --build 

echo "[+] Docker Compose is now running in detached mode."
