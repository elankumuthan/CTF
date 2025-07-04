# CTF Web Environment — Docker Compose Setup

This project runs a multi-service Capture-The-Flag (CTF) web environment using Docker Compose. It includes decoy services, hidden vulnerabilities, and CTF-style misdirection.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo-name/ctf-docker.git
cd ctf-docker
```

This command builds all services and starts them using Docker Compose.

### 2. Start the Containers

```bash
docker-compose up --build
```

## Shut Down

To stop all running containers:

```bash
docker-compose down
```

To stop containers and remove all associated volumes:

```bash
docker-compose down -v
```


## Prerequisites

- Docker
- Docker Compose
- socat (for decoy services)

## Notes

- This environment is designed for educational CTF purposes
- Decoy services are intentionally designed to waste attackers' time
- Make sure to run this in a controlled environment only

## Security Warning

This environment contains intentionally vulnerable services. Only run in isolated environments and never expose to public networks.

