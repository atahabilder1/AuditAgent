# Chapter 2: Installation & Setup

[← Previous: Introduction](01-introduction.md) | [Home](../README.md) | [Next: Quick Start →](03-quickstart.md)

---

## Table of Contents
- [2.1 Hardware Requirements](#21-hardware-requirements)
- [2.2 Software Prerequisites](#22-software-prerequisites)
- [2.3 Step-by-Step Installation](#23-step-by-step-installation)
  - [2.3.1 Automated Setup (Recommended)](#231-automated-setup-recommended)
  - [2.3.2 Manual Installation](#232-manual-installation)
- [2.4 Verification & Testing](#24-verification--testing)
- [2.5 Troubleshooting](#25-troubleshooting)
- [2.6 Docker Installation](#26-docker-installation)

---

## 2.1 Hardware Requirements

### Your Current Setup

You mentioned you have:
- **GPU**: NVIDIA RTX A6000 (48GB VRAM) ✅ Perfect!
- **RAM**: 64 GB ✅ Excellent
- **Storage**: 468 GB free on /data partition ✅ Sufficient
- **OS**: Ubuntu 24.04 ✅ Supported

This is an **ideal setup** for AuditAgent v2.0!

### Minimum Requirements

To run AuditAgent v2.0, you need **at minimum**:

| Component | Minimum | Your Setup | Status |
|-----------|---------|------------|--------|
| GPU | NVIDIA RTX 3090 (24GB) | RTX A6000 (48GB) | ✅ Excellent |
| VRAM | 24GB | 48GB | ✅ 2x requirement |
| RAM | 32GB | 64GB | ✅ 2x requirement |
| Storage | 200GB | 468GB | ✅ 2.3x requirement |
| CUDA | 11.8+ | Check below | ⏳ Will verify |
| OS | Ubuntu 20.04+ | Ubuntu 24.04 | ✅ Latest LTS |

### Storage Breakdown

Here's how the 200GB minimum breaks down:

```
/data/AuditAgent/                   Total: ~200GB
├── venv/                           ~3GB    (Python packages)
├── src/                            ~50MB   (Source code)
├── /data/llm_models/
│   └── qwen2.5-coder-32b/         ~19GB   (LLM model)
├── /home/user/.foundry/            ~1GB    (Foundry cache)
├── audit_reports/                  ~1GB    (Per 1000 contracts)
└── datasets/ (optional)            ~10GB   (Fine-tuning data)
```

💡 **Tip**: Use the `/data` partition as you mentioned - it has plenty of space!

---

## 2.2 Software Prerequisites

### Operating System Check

```bash
# Check your OS version
lsb_release -a
# Should show: Ubuntu 24.04 LTS

# Check kernel version
uname -r
# Should show: 6.x.x or higher
```

### GPU & CUDA Check

```bash
# Check NVIDIA driver
nvidia-smi

# Expected output:
# +-----------------------------------------------------------------------------+
# | NVIDIA-SMI 535.xx       Driver Version: 535.xx       CUDA Version: 12.x  |
# +-----------------------------------------------------------------------------+
# | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
# | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
# |===============================+======================+======================|
# |   0  NVIDIA RTX A6000    Off  | 00000000:01:00.0 Off |                  Off |
# | 30%   35C    P8    25W / 300W |      0MiB / 49140MiB |      0%      Default |
# +-----------------------------------------------------------------------------+
```

✅ **If you see your GPU**: Proceed to installation
❌ **If you get "command not found"**: Install NVIDIA drivers first (see Troubleshooting)

### Python Check

```bash
# Check Python version
python3 --version
# Required: Python 3.10 or 3.11
# Ubuntu 24.04 comes with Python 3.12, which should work but is less tested

# If you need Python 3.10 specifically:
sudo apt install python3.10 python3.10-venv python3.10-dev
```

---

## 2.3 Step-by-Step Installation

You have **two options**: Automated (recommended) or Manual.

### 2.3.1 Automated Setup (Recommended)

We've created a script that installs everything for you!

#### Step 1: Navigate to Project

```bash
cd /data/AuditAgent
```

#### Step 2: Run Setup Script

```bash
# Make the script executable
chmod +x scripts/setup_environment.sh

# Run it (will take 10-30 minutes)
./scripts/setup_environment.sh
```

#### What the Script Does

The setup script will:

1. ✅ Install system dependencies (build tools, libraries)
2. ✅ Create Python virtual environment in `/data/AuditAgent/venv`
3. ✅ Install all Python packages from `requirements.txt`
4. ✅ Install Foundry (Forge, Cast, Anvil)
5. ✅ Install Ollama (LLM server)
6. ✅ Pull Qwen2.5-Coder-32B model (~19GB download)
7. ✅ Install Slither static analyzer
8. ✅ Initialize Foundry project for sandbox testing
9. ✅ Create `.env` configuration file

#### Expected Output

You'll see output like this:

```
=========================================
AuditAgent v2.0 Environment Setup
=========================================

Step 1: Installing system dependencies...
✓ System packages installed

Step 2: Setting up Python virtual environment...
✓ Virtual environment created at /data/AuditAgent/venv

Step 3: Installing Python dependencies...
✓ Python packages installed (this may take 5-10 minutes)

Step 4: Installing Foundry...
✓ Foundry installed successfully
forge 0.2.0 (...)

Step 5: Installing Ollama...
✓ Ollama installed successfully

Step 6: Pulling Qwen2.5-Coder-32B model...
⚠  This will download ~19GB - may take 10-30 minutes depending on internet speed
pulling manifest
pulling 8934d96d3f08... 100% ▕████████████████████████████████████████████████▏
pulling 8c17c2ebb0ea... 100% ▕████████████████████████████████████████████████▏
pulling 7c23fb36d801... 100% ▕████████████████████████████████████████████████▏
pulling 2e0493f67d0c... 100% ▕████████████████████████████████████████████████▏
pulling fa8235e5b48f... 100% ▕████████████████████████████████████████████████▏
✓ Model downloaded to /data/llm_models

Step 7: Installing Slither...
✓ Slither installed successfully

Step 8: Initializing Foundry project...
✓ Foundry project initialized

Step 9: Creating configuration files...
✓ .env file created

=========================================
Setup Complete!
=========================================

Next steps:
1. Activate virtual environment: source venv/bin/activate
2. Update .env file with your API keys (optional)
3. Run a test audit: python examples/basic_usage.py

Hardware detected:
GPU 0: NVIDIA RTX A6000, 49140MiB

Note: Ensure Ollama is running before starting audits:
  ollama serve
```

#### Step 3: Activate Environment

```bash
# Activate the virtual environment
source venv/bin/activate

# Your prompt should change to:
(venv) user@hostname:/data/AuditAgent$
```

#### Step 4: Verify Installation

Jump to [Section 2.4](#24-verification--testing)

---

### 2.3.2 Manual Installation

If the automated script fails or you prefer manual control:

#### Step 1: System Dependencies

```bash
# Update package list
sudo apt update

# Install build essentials
sudo apt install -y \
    python3-dev \
    python3-pip \
    python3-venv \
    build-essential \
    libssl-dev \
    libffi-dev \
    git \
    curl \
    wget
```

#### Step 2: Create Virtual Environment

```bash
cd /data/AuditAgent

# Create venv
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

#### Step 3: Install Python Dependencies

```bash
# Install all packages (takes 5-10 minutes)
pip install -r requirements.txt

# If you get errors, install in stages:
# 1. Core dependencies
pip install web3 requests pyyaml python-dotenv

# 2. Analysis tools
pip install slither-analyzer

# 3. LLM client
pip install ollama

# 4. UI and utilities
pip install rich click colorama tabulate

# 5. Optional: Fine-tuning (large downloads)
pip install torch transformers datasets peft trl
```

#### Step 4: Install Foundry

```bash
# Download and install Foundry
curl -L https://foundry.paradigm.xyz | bash

# Add to PATH (add to ~/.bashrc for persistence)
export PATH="$HOME/.foundry/bin:$PATH"

# Install/update Foundry tools
foundryup

# Verify
forge --version
anvil --version
cast --version
```

#### Step 5: Install Ollama

```bash
# Download and install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify
ollama --version
```

#### Step 6: Configure Ollama for /data Storage

```bash
# Set Ollama models directory to /data
export OLLAMA_MODELS=/data/llm_models
mkdir -p /data/llm_models

# Make it permanent (add to ~/.bashrc)
echo 'export OLLAMA_MODELS=/data/llm_models' >> ~/.bashrc
```

#### Step 7: Pull Qwen Model

```bash
# Start Ollama server in background
ollama serve &

# Wait a few seconds
sleep 5

# Pull the model (19GB download)
ollama pull qwen2.5-coder:32b-instruct

# This will take 10-30 minutes depending on internet speed
# You'll see progress:
# pulling manifest
# pulling 8934d96d3f08... 42% ▕█████████████████████▏
```

#### Step 8: Install Slither

```bash
pip install slither-analyzer

# Verify
slither --version
```

#### Step 9: Initialize Foundry Project

```bash
cd src/sandbox/foundry_project

# Install Forge standard library
forge install foundry-rs/forge-std --no-commit

cd ../../..
```

#### Step 10: Create Configuration

```bash
# Create .env file
cat > .env << 'EOF'
# AuditAgent v2.0 Configuration

# Blockchain RPC URLs (optional - defaults provided)
ETHEREUM_RPC_URL=https://eth.llamarpc.com
BSC_RPC_URL=https://bsc-dataseed.binance.org
POLYGON_RPC_URL=https://polygon-rpc.com

# Etherscan API Keys (optional - for fetching verified contracts)
ETHERSCAN_API_KEY=your_etherscan_api_key_here
BSCSCAN_API_KEY=your_bscscan_api_key_here

# Ollama Configuration
OLLAMA_MODELS=/data/llm_models
OLLAMA_HOST=http://localhost:11434

# Model Configuration
LLM_MODEL=qwen2.5-coder:32b-instruct
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=4096

# Output Configuration
OUTPUT_DIR=./audit_reports
VERBOSE=true
EOF

echo ".env file created!"
```

---

## 2.4 Verification & Testing

Let's verify everything is installed correctly.

### Test 1: Python Environment

```bash
# Activate venv if not already
source venv/bin/activate

# Check Python packages
python -c "import web3; import ollama; import rich; print('✅ Core packages OK')"

# Expected: ✅ Core packages OK
```

### Test 2: Slither

```bash
# Test Slither
slither --version

# Expected: 0.9.x or higher
```

### Test 3: Foundry

```bash
# Test Forge
forge --version

# Expected: forge 0.2.0 ...

# Test Anvil
anvil --version

# Expected: anvil 0.2.0 ...
```

### Test 4: Ollama & Model

```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# If you get "connection refused", start Ollama:
ollama serve &

# Check if model is downloaded
ollama list

# Expected output:
# NAME                           ID              SIZE    MODIFIED
# qwen2.5-coder:32b-instruct    8934d96d3f08    19 GB   X minutes ago
```

### Test 5: Quick LLM Test

```bash
# Test the LLM (should respond instantly if model is loaded)
ollama run qwen2.5-coder:32b-instruct "Write a function that adds two numbers"

# Expected: Code output in a few seconds
```

### Test 6: GPU Utilization

```bash
# While LLM is running, check GPU usage
nvidia-smi

# You should see ollama process using ~22-25GB VRAM
```

### Test 7: AuditAgent Modules

```bash
cd /data/AuditAgent

# Test LLM module
python -c "from src.llm.ollama_client import OllamaClient; print('✅ LLM module OK')"

# Test economic module
python -c "from src.economic.dex_price_fetcher import DEXPriceFetcher; print('✅ Economic module OK')"

# Test exploiter module
python -c "from src.exploiter.exploit_generator import ExploitGenerator; print('✅ Exploiter module OK')"

# Test sandbox module
python -c "from src.sandbox.chain_forker import ChainForker; print('✅ Sandbox module OK')"

# All should print ✅
```

### Test 8: Full System Test

```bash
# Run a simple audit on test contract
python examples/basic_usage.py

# Expected output:
# [AuditAgent] Starting security audit for: tests/contracts/VulnerableBank.sol
# ==================================================================================
# [Phase 1/4] Running Slither static analysis...
#   ✓ Found X potential issues
# [Phase 2/4] Running Mythril symbolic execution...
#   ✓ Found X potential issues
# [Phase 3/4] Running vulnerability pattern detection...
#   ✓ Detected X vulnerability patterns
# [Phase 4/4] Running AI-powered security analysis...
#   ✓ AI analysis completed with X recommendations
# ==================================================================================
# [AuditAgent] Audit complete! Total vulnerabilities: X
```

---

## 2.5 Troubleshooting

### Issue 1: NVIDIA Driver Not Found

**Symptom**: `nvidia-smi` says "command not found"

**Solution**:
```bash
# Check if driver is installed
dpkg -l | grep nvidia-driver

# If not, install latest driver
sudo ubuntu-drivers devices
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# After reboot, verify
nvidia-smi
```

### Issue 2: Ollama Model Download Fails

**Symptom**: "Error pulling model" or timeout

**Solution**:
```bash
# Check internet connection
ping -c 3 ollama.com

# Try with verbose output
OLLAMA_DEBUG=1 ollama pull qwen2.5-coder:32b-instruct

# If still fails, download manually:
# Visit: https://ollama.com/library/qwen2.5-coder
```

### Issue 3: Out of VRAM

**Symptom**: "CUDA out of memory" when running LLM

**Solution**:
```bash
# Check current VRAM usage
nvidia-smi

# Kill any GPU processes
pkill -9 ollama

# Free up VRAM and restart
ollama serve &
```

### Issue 4: Python Package Conflicts

**Symptom**: Dependency resolver errors during `pip install`

**Solution**:
```bash
# Delete venv and start fresh
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Install in specific order
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
```

### Issue 5: Foundry Installation Fails

**Symptom**: `foundryup` command not found after install

**Solution**:
```bash
# Manually download
cd ~
curl -L https://foundry.paradigm.xyz -o foundry.sh
bash foundry.sh

# Restart shell or source profile
source ~/.bashrc

# Try again
foundryup
```

### Issue 6: Permission Denied on /data

**Symptom**: Cannot write to `/data/llm_models`

**Solution**:
```bash
# Check ownership
ls -ld /data

# Fix ownership (replace 'youruser' with your username)
sudo chown -R youruser:youruser /data/AuditAgent
sudo chown -R youruser:youruser /data/llm_models
```

### Issue 7: Slither Not Finding Solidity Files

**Symptom**: "No contracts found" when running Slither

**Solution**:
```bash
# Install Solc (Solidity compiler)
pip install solc-select
solc-select install 0.8.20
solc-select use 0.8.20

# Verify
solc --version
```

---

## 2.6 Docker Installation

If you prefer containerized deployment:

### Prerequisites

```bash
# Install Docker
sudo apt install docker.io docker-compose

# Install NVIDIA Docker runtime (for GPU)
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Build and Run

```bash
cd /data/AuditAgent/docker

# Build images
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# Pull model inside container
docker exec audit-agent ollama pull qwen2.5-coder:32b-instruct

# Run audit
docker exec -it audit-agent python3 examples/basic_usage.py
```

See [Chapter 17: Docker Deployment](17-docker.md) for complete details.

---

## Summary

You should now have:
- ✅ All system dependencies installed
- ✅ Python virtual environment set up
- ✅ Foundry (Forge, Anvil, Cast) installed
- ✅ Ollama running with Qwen 32B model
- ✅ Slither static analyzer ready
- ✅ All Python modules tested
- ✅ GPU properly configured

**Installation time**: 30-60 minutes (mostly model download)
**Disk usage**: ~25-30GB

### What's Next?

Now that everything is installed, you're ready to:

1. **[Chapter 3: Quick Start →](03-quickstart.md)** - Run your first audit
2. **[Chapter 11: Tutorials →](11-tutorials.md)** - Step-by-step examples
3. **[Chapter 4: Architecture →](04-architecture.md)** - Understand how it works

---

💡 **Pro Tip**: Add to your ~/.bashrc for convenience:

```bash
# AuditAgent aliases
alias audit-activate='cd /data/AuditAgent && source venv/bin/activate'
alias audit-serve='ollama serve &'
alias audit-run='python -m src.audit_agent'

# Then you can just type: audit-activate
```

---

[← Previous: Introduction](01-introduction.md) | [Home](../README.md) | [Next: Quick Start →](03-quickstart.md)
