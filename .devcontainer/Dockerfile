# Use Ubuntu 22.04 as base image for better compatibility
FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV OLLAMA_HOST=0.0.0.0:11434
ENV PATH=/usr/local/bin:$PATH

# Update system packages
RUN apt-get update && apt-get upgrade -y

# Install essential packages
RUN apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    software-properties-common \
    ca-certificates \
    gnupg \
    lsb-release \
    sudo \
    vim \
    nano \
    htop \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.11 and pip
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Upgrade pip
RUN python -m pip install --upgrade pip setuptools wheel

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Create directories for Ollama
RUN mkdir -p /root/.ollama

# Copy requirements and install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Install additional packages for enhanced interface
RUN pip install \
    gradio==4.7.1 \
    python-docx==1.1.0 \
    PyPDF2==3.0.1 \
    watchdog==3.0.0 \
    jupyter==1.0.0

# Create workspace directory
RUN mkdir -p /workspaces/ai-summarizer-workshop
WORKDIR /workspaces/ai-summarizer-workshop

# Set permissions for vscode user
RUN chown -R vscode:vscode /workspaces/ai-summarizer-workshop

# Expose ports for Streamlit, Gradio, and Ollama
EXPOSE 8501 8502 7860 11434

# Create entrypoint script
RUN echo '#!/bin/bash\n\
# Start Ollama service in background\n\
ollama serve &\n\
sleep 5\n\
\n\
# Keep container running\n\
exec "$@"' > /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["sleep", "infinity"]