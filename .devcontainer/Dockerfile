# Use the official Python 3.12 image based on Debian (more compatible than Alpine)
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  NODE_VERSION=20.19.1 \
  NPM_VERSION=11.3.0 \
  NVM_DIR="/usr/local/share/nvm" \
  DJANGO_SETTINGS_MODULE=greenova.settings

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
  && apt-get -y install --no-install-recommends \
  fish \
  direnv \
  python3-pip \
  python3-venv \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Ensure pip is properly installed and upgraded
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Set up Node.js using the pre-installed NVM
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION} \
  && nvm alias default ${NODE_VERSION} \
  && npm install -g npm@${NPM_VERSION}

# Create required directories for fish shell
RUN mkdir -p /home/vscode/.config/fish /home/vscode/.config/fish/functions /home/vscode/.local/share/fish \
  && chown -R vscode:vscode /home/vscode/.config /home/vscode/.local

# We'll install Python dependencies after the workspace is mounted
# in the postCreateCommand or postStartCommand

# Make prepare vscode user for development
USER vscode

# Ensure fish shell is properly configured
RUN echo 'set -gx PATH /usr/local/share/nvm/versions/node/v${NODE_VERSION}/bin $PATH' > /home/vscode/.config/fish/config.fish \
  && echo 'set -gx NODE_PATH /usr/local/share/nvm/versions/node/v${NODE_VERSION}/lib/node_modules' >> /home/vscode/.config/fish/config.fish \
  && echo 'set -gx PYTHONPATH /workspaces/greenova:/workspaces/greenova/greenova $PYTHONPATH' >> /home/vscode/.config/fish/config.fish \
  && echo 'set -gx PYTHONSTARTUP /workspaces/greenova/pythonstartup' >> /home/vscode/.config/fish/config.fish

# Set working directory
WORKDIR /workspaces/greenova

# Switch back to root to ensure entrypoint can handle permissions properly
USER root

# Copy entrypoint script using relative path from .devcontainer directory
COPY .devcontainer/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Switch back to vscode user for operations
USER vscode

# Default command
CMD ["sleep", "infinity"]
