FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    curl \
    wget \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Foundry
RUN curl -L https://foundry.paradigm.xyz | bash && \
    /root/.foundry/bin/foundryup

ENV PATH="/root/.foundry/bin:${PATH}"

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy application files
COPY requirements.txt .
COPY src/ ./src/
COPY examples/ ./examples/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Create directories for models and data
RUN mkdir -p /data/llm_models /data/audit_reports

# Set environment variables
ENV OLLAMA_MODELS=/data/llm_models
ENV PYTHONPATH=/app

# Expose ports (Ollama, Anvil)
EXPOSE 11434 8545

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ollama list || exit 1

# Default command
CMD ["bash"]
