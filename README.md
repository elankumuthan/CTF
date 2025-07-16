# CTF Web Environment — Docker Compose Setup

This project runs a multi-service Capture-The-Flag (CTF) web environment using Docker Compose. It includes decoy services, hidden vulnerabilities, and CTF-style misdirection.

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo-name/ctf-docker.git
cd ctf-docker
```

### 3. Start the CTF Environment
This starts the CTF environment and enables stealth mode.
```bas
RUNME.sh
```

## Shut Down

### 1. Stop the CTF Environment
```bash
KILLME.sh
```

### Optional: Remove All Data
To completely remove containers and volumes:
```bash
docker-compose down -v
```

## Prerequisites

- Docker
- Docker Compose
- socat (for decoy services)

## What's Included

- **Stealth Protection**: Blocks ping and port scans to hide your containers
- **Decoy Services**: Intentionally designed to waste attackers' time
- **Hidden Vulnerabilities**: CTF-style challenges and misdirection

## Security Warning

This environment contains intentionally vulnerable services. Only run in isolated environments and never expose to public networks.

## Notes

- Run stealth mode before starting containers for maximum effect
- Always disable stealth mode when finished to avoid affecting other services
- This environment is designed for educational CTF purposes only

## Security Warning

This environment contains intentionally vulnerable services. Only run in isolated environments and never expose to public networks.

