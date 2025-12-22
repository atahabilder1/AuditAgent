#!/bin/bash
# AuditAgent v2.0 Environment Setup Script
# One-click setup for the entire audit environment

set -e  # Exit on error

echo "========================================="
echo "AuditAgent v2.0 Environment Setup"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Ubuntu
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [ "$ID" != "ubuntu" ]; then
        echo -e "${YELLOW}Warning: This script is optimized for Ubuntu. Proceed with caution.${NC}"
    fi
fi

echo -e "${GREEN}Step 1: Installing system dependencies...${NC}"
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    python3-pip \
    python3-venv \
    build-essential \
    libssl-dev \
    libffi-dev \
    git \
    curl \
    wget

echo -e "${GREEN}Step 2: Setting up Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

source venv/bin/activate

echo -e "${GREEN}Step 3: Installing Python dependencies...${NC}"
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo -e "${GREEN}Step 4: Installing Foundry (Forge, Cast, Anvil)...${NC}"
if ! command -v forge &> /dev/null; then
    echo "Installing Foundry..."
    curl -L https://foundry.paradigm.xyz | bash
    export PATH="$HOME/.foundry/bin:$PATH"
    foundryup
    echo -e "${GREEN}Foundry installed successfully${NC}"
else
    echo "Foundry already installed"
    forge --version
fi

echo -e "${GREEN}Step 5: Installing Ollama...${NC}"
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "${GREEN}Ollama installed successfully${NC}"
else
    echo "Ollama already installed"
    ollama --version
fi

echo -e "${GREEN}Step 6: Pulling Qwen2.5-Coder-32B model...${NC}"
echo -e "${YELLOW}This may take a while (model is ~19GB)...${NC}"

# Set Ollama models directory to /data
export OLLAMA_MODELS=/data/llm_models
mkdir -p /data/llm_models

# Pull the model
ollama pull qwen2.5-coder:32b-instruct

echo -e "${GREEN}Step 7: Installing Slither...${NC}"
if ! command -v slither &> /dev/null; then
    pip install slither-analyzer
    echo -e "${GREEN}Slither installed successfully${NC}"
else
    echo "Slither already installed"
    slither --version
fi

echo -e "${GREEN}Step 8: Initializing Foundry project...${NC}"
cd src/sandbox/foundry_project
if [ ! -d "lib" ]; then
    forge install foundry-rs/forge-std --no-commit
fi
cd ../../..

echo -e "${GREEN}Step 9: Creating configuration files...${NC}"
if [ ! -f ".env" ]; then
    cat > .env << EOF
# AuditAgent v2.0 Configuration

# Blockchain RPC URLs (optional - defaults are provided)
ETHEREUM_RPC_URL=https://eth.llamarpc.com
BSC_RPC_URL=https://bsc-dataseed.binance.org
POLYGON_RPC_URL=https://polygon-rpc.com

# Etherscan API Keys (optional)
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
    echo ".env file created - please update with your API keys"
else
    echo ".env file already exists"
fi

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Update .env file with your API keys (optional)"
echo "3. Run a test audit: python examples/basic_usage.py"
echo ""
echo "Hardware detected:"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "No NVIDIA GPU detected"
echo ""
echo -e "${YELLOW}Note: Ensure Ollama is running before starting audits:${NC}"
echo "  ollama serve"
echo ""
