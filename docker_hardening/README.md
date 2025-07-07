# Docker Hardening Scripts

Make your Docker containers invisible to basic network scans like ping and Nmap.

## What it does

These scripts block common reconnaissance techniques:
- Ping requests (ICMP)
- Port scans on ports 80 and 443
- Makes containers appear offline to attackers

## Quick Start

**To enable protection:**
```bash
chmod +x harden_docker.sh
./harden_docker.sh
```

**To remove protection:**
```bash
chmod +x unharden_docker.sh
./unharden_docker.sh
```

## Requirements

- Ubuntu/Debian Linux
- Docker installed
- Root access (sudo)

## Files

- `harden_docker.sh` - Enable stealth mode
- `unharden_docker.sh` - Disable stealth mode
- `README.md` - This file

## How it works

The scripts modify your host firewall rules (not the containers themselves) to drop specific network packets that scanners use to detect running services.

