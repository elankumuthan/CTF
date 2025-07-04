# 🐳 CTF Web Environment — Docker Compose Setup

This project runs a multi-service Capture-The-Flag (CTF) web environment using Docker Compose. It includes decoy services, hidden vulnerabilities, and CTF-style misdirection.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo-name/ctf-docker.git
cd ctf-docker
```

### 2. Start the Containers

```bash
docker-compose up --build
```

This command builds all services and starts them using Docker Compose.

## 📦 Shut Down

To stop all running containers:

```bash
docker-compose down
```

To stop containers and remove all associated volumes:

```bash
docker-compose down -v
```

## 🎯 CTF Services Overview

### Decoy Services

The environment includes various honeypot services designed to mislead attackers:

- **FTP Decoy (Port 21)** - Interactive honeypot that wastes time
- **SSH Decoy (Port 22)** - Slow connection that hangs then disconnects

### Starting CTF Decoy Services

To manually start the decoy services:

```bash
#!/bin/bash
echo "Starting CTF decoy services..."

# FTP (21) - Interactive honeypot that wastes time
socat TCP-LISTEN:21,fork,reuseaddr EXEC:"/opt/services/ftp_decoy.sh" &
echo "FTP decoy started on port 21"

# SSH (22) - Slow connection that hangs then disconnects
# Add your SSH decoy implementation here
```

## 🔧 Prerequisites

- Docker
- Docker Compose
- socat (for decoy services)

## 📝 Notes

- This environment is designed for educational CTF purposes
- Decoy services are intentionally designed to waste attackers' time
- Make sure to run this in a controlled environment only

## 🛡️ Security Warning

This environment contains intentionally vulnerable services. Only run in isolated environments and never expose to public networks.

## 📄 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]