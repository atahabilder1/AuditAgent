# Docker Setup for AuditAgent v2.0

This directory contains Docker configuration for running AuditAgent in a containerized environment.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 1.29+
- NVIDIA Docker runtime (for GPU support)

## Quick Start

1. Build and start all services:
```bash
docker-compose up -d
```

2. Pull the Qwen model (first time only):
```bash
docker exec audit-agent ollama pull qwen2.5-coder:32b-instruct
```

3. Run an audit:
```bash
docker exec -it audit-agent python3 examples/basic_usage.py
```

## Services

### audit-agent
Main application container with:
- Python 3.10
- Foundry (Forge, Cast, Anvil)
- Slither
- All Python dependencies

### ollama
LLM inference service:
- Runs Qwen2.5-Coder-32B locally
- Requires GPU (NVIDIA)
- Exposed on port 11434

### anvil
Blockchain forking service:
- Local Ethereum/BSC/Polygon fork
- Exposed on port 8545

## Usage

### Interactive Shell
```bash
docker exec -it audit-agent bash
```

### Run Audit
```bash
docker exec audit-agent python3 -m src.audit_agent <contract_path>
```

### View Logs
```bash
docker-compose logs -f audit-agent
```

## Volumes

- `llm-models`: Stores downloaded LLM models (persistent)
- `audit-reports`: Stores audit reports (persistent)

## GPU Support

The Ollama container requires NVIDIA GPU. Ensure nvidia-docker2 is installed:

```bash
# Install NVIDIA Docker runtime
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

## Troubleshooting

### Ollama not starting
Check GPU availability:
```bash
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### Models not persisting
Ensure volumes are properly mounted:
```bash
docker volume ls
docker volume inspect audit-agent_llm-models
```

### Network issues
Reset network:
```bash
docker-compose down
docker network prune
docker-compose up -d
```

## Cleanup

Stop and remove all containers:
```bash
docker-compose down
```

Remove volumes (WARNING: deletes models and reports):
```bash
docker-compose down -v
```
