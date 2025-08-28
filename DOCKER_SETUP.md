# Docker-based Smart Contract Verification Setup Guide

This guide explains how to run the DbC-GPT-v2 smart contract verification system using Docker containers for isolated, reproducible experiments.

## Overview

The DbC-GPT-v2 project uses Docker containers to provide:
- **Isolated verification environments** with solc-verify tools
- **Parallel experiment execution** across multiple containers
- **Reproducible research environments** for consistent results
- **Easy deployment** without complex local setup

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)
- OpenAI API key (set in environment variables)
- Git (to clone the repository)

## Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd DbC-GPT-v2

# Set up environment variables
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 2. Docker Container Options

The project provides several Docker configurations:

#### Option A: Pre-built Verification Environment
```bash
# Build the main verification container
docker build -t dbc-gpt-verifier .

# Run with mounted workspace
docker run -it --name verification-container \
  -v $(pwd):/workspace \
  -w /workspace \
  --env-file .env \
  dbc-gpt-verifier bash
```

#### Option B: Solc-Verify Specific Versions
```bash
# For Solidity 0.5 compatibility
docker build -f experiments/solc_verify_generator/Dockerfile_0.5 \
  -t solc-verify-0.5 .

# For Solidity 0.7 compatibility
docker build -f experiments/solc_verify_generator/Dockerfile_0.7 \
  -t solc-verify-0.7 .
```

#### Option C: Docker Compose Stack (Recommended)
```bash
# Create docker-compose.yml
cat > docker-compose.yml << EOF
services:
  verification-runner:
    image: python:3.9-slim
    container_name: dbc-gpt-runner
    volumes:
      - .:/workspace
    working_dir: /workspace
    environment:
      - PYTHONPATH=/workspace
      - OPENAI_API_KEY=\${OPENAI_API_KEY}
    command: tail -f /dev/null
  
  verification-monitor:
    image: ubuntu:focal
    container_name: verification-monitor
    volumes:
      - .:/workspace
    working_dir: /workspace
    environment:
      - PYTHONPATH=/workspace
    command: tail -f /dev/null
EOF

# Deploy the stack
docker-compose up -d
```

## Running Verification Experiments

### Basic Verification Run

```bash
# Enter the verification container
docker exec -it dbc-gpt-runner bash

# Install Python dependencies
pip install -r requirements.txt

# Run a basic ERC20 verification
cd experiments
python3 loop_contract_verifier.py \
  --requested erc20 \
  --context "erc20" \
  --runs 1 \
  --max-iterations 2
```

### Advanced Verification Options

#### Multiple ERC Standards
```bash
# ERC721 verification
python3 loop_contract_verifier.py \
  --requested erc721 \
  --context "erc721" \
  --runs 5 \
  --max-iterations 10

# ERC1155 verification
python3 loop_contract_verifier.py \
  --requested erc1155 \
  --context "erc1155" \
  --runs 3 \
  --max-iterations 5
```

#### Function-by-Function Verification
```bash
# Run function-level verification
python3 func_by_func_verifier.py \
  --requested erc20 \
  --context "erc20" \
  --runs 2 \
  --max-iterations 3
```

#### Using Different AI Assistants
```bash
# Use fine-tuned assistant
python3 loop_contract_verifier.py \
  --requested erc20 \
  --context "erc20" \
  --assistant "erc-20-001-5-16" \
  --runs 1 \
  --max-iterations 5
```

## Container Management

### Monitoring Experiments

```bash
# Check running containers
docker ps

# View container logs
docker logs dbc-gpt-runner
docker logs verification-monitor

# Monitor resource usage
docker stats
```

### Parallel Execution

```bash
# Run multiple verification instances
for i in {1..3}; do
  docker run -d --name "verifier-$i" \
    -v $(pwd):/workspace \
    -w /workspace/experiments \
    --env-file .env \
    python:3.9-slim \
    python3 loop_contract_verifier.py \
      --requested erc20 \
      --context "erc20" \
      --runs 1 \
      --max-iterations 2
done
```

### Data Persistence

Results are automatically saved to the host filesystem:

```bash
# Verification results
ls experiments/results_entire_contract/
ls experiments/results_func_by_func_*/

# Thread conversations
ls experiments/threads_entire_contract/
ls experiments/threads_func_by_func_*/
```

## Configuration Options

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional
SOLC_VERIFY_TIMEOUT=120  # Verification timeout in seconds
PYTHONPATH=/workspace    # Python module path
```

### Volume Mounts

```bash
# Mount specific directories
docker run -v $(pwd)/experiments:/workspace/experiments \
           -v $(pwd)/assets:/workspace/assets \
           -v $(pwd)/data:/workspace/data \
           dbc-gpt-verifier
```

## Troubleshooting

### Common Issues

1. **Missing OpenAI API Key**
   ```bash
   # Check environment variables
   docker exec dbc-gpt-runner env | grep OPENAI
   ```

2. **File Permission Issues**
   ```bash
   # Fix permissions
   sudo chown -R $USER:$USER experiments/results_*
   ```

3. **Container Resource Limits**
   ```bash
   # Increase memory limit
   docker run --memory=4g --cpus=2 dbc-gpt-verifier
   ```

4. **Solc-Verify Not Found**
   ```bash
   # Use the specialized Dockerfile
   docker build -f experiments/solc_verify_generator/Dockerfile_0.5 \
     -t solc-verify .
   ```

### Debugging

```bash
# Interactive debugging session
docker exec -it dbc-gpt-runner bash

# Check Python environment
python3 -c "import openai; print('OpenAI library available')"

# Test solc-verify (if installed)
solc-verify.py --version
```

## Performance Optimization

### Resource Allocation

```bash
# Optimize for multiple parallel runs
docker-compose up --scale verification-runner=3

# Limit resources per container
docker run --cpus=1 --memory=2g dbc-gpt-verifier
```

### Batch Processing

```bash
# Process multiple contracts in batch
for contract in erc20 erc721 erc1155; do
  docker run --name "batch-$contract" \
    -v $(pwd):/workspace \
    -w /workspace/experiments \
    --env-file .env \
    python:3.9-slim \
    python3 loop_contract_verifier.py \
      --requested $contract \
      --context "$contract" \
      --runs 5 \
      --max-iterations 10 &
done
wait  # Wait for all background jobs to complete
```

## Results Analysis

### Accessing Results

```bash
# View CSV results
docker exec dbc-gpt-runner cat experiments/results_entire_contract/4o-mini/erc20/erc20/erc20_[erc20].csv

# Analyze with pandas
docker exec dbc-gpt-runner python3 -c "
import pandas as pd
df = pd.read_csv('experiments/results_entire_contract/4o-mini/erc20/erc20/erc20_[erc20].csv')
print(df.describe())
"
```

### Comparison Tools

```bash
# Run assistant comparison
docker exec dbc-gpt-runner python3 compare_assistants.py

# Context comparison
docker exec dbc-gpt-runner python3 compare_contexts.py
```

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove all verification containers
docker rm $(docker ps -a -q --filter="name=verifier")

# Clean up images
docker rmi dbc-gpt-verifier solc-verify-0.5 solc-verify-0.7

# Remove volumes (careful - this deletes data!)
docker volume prune
```

## Security Considerations

- **API Keys**: Never commit API keys to version control
- **Network**: Use `--network none` for isolated experiments
- **Volumes**: Mount only necessary directories
- **User**: Run containers with non-root user when possible

```bash
# Secure container run
docker run --user $(id -u):$(id -g) \
           --network none \
           -v $(pwd)/experiments:/workspace/experiments:ro \
           dbc-gpt-verifier
```

## Next Steps

1. **Scale Up**: Use Kubernetes for large-scale experiments
2. **CI/CD**: Integrate with GitHub Actions for automated testing
3. **Monitoring**: Add Prometheus/Grafana for experiment monitoring
4. **Results**: Set up automated result analysis and reporting

For more information, see the main [README.md](README.md) and project documentation.