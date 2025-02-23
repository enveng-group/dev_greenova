FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Install build essentials and make
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    shellcheck \
    shfmt

# Install Python
ARG PYTHON_VERSION=3.13.2
RUN apt-get install -y python${PYTHON_VERSION} python3-pip

# Install Git
ARG GIT_VERSION=2.48.1
RUN add-apt-repository ppa:git-core/ppa && \
    apt-get update && \
    apt-get install -y git=${GIT_VERSION}*

# Install Node.js via nvm
ARG NODE_VERSION=23.8.0
ARG NVM_VERSION=0.40.1
ARG PNPM_VERSION=10.4.1
ENV NVM_DIR=/usr/local/share/nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v${NVM_VERSION}/install.sh | bash && \
    . $NVM_DIR/nvm.sh && \
    nvm install ${NODE_VERSION} && \
    nvm alias default ${NODE_VERSION} && \
    npm install -g pnpm@${PNPM_VERSION}

# Create scripts directory
RUN mkdir -p /workspaces/scripts && \
    chown -R vscode:vscode /workspaces/scripts

# Set up workspace for Makefile
COPY Makefile /workspaces/
RUN chown vscode:vscode /workspaces/Makefile

USER vscode

# Initialize workspace
WORKDIR /workspaces
RUN mkdir -p logs && \
    chmod +x scripts/*.sh 2>/dev/null || true

# Set up SSH and Git
RUN apt-get update && apt-get install -y \
    openssh-client \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set up dotfiles directory
RUN mkdir -p /home/vscode/dotfiles && \
    chown -R vscode:vscode /home/vscode/dotfiles

# Set up SSH directory permissions
RUN mkdir -p /home/vscode/.ssh && \
    chmod 700 /home/vscode/.ssh && \
    chown -R vscode:vscode /home/vscode/.ssh

# Create SSH config for GitHub
RUN echo "Host github.com\n\
    StrictHostKeyChecking no\n\
    UserKnownHostsFile=/dev/null\n\
    IdentityFile ~/.ssh/id_ed25519" > /home/vscode/.ssh/config && \
    chmod 600 /home/vscode/.ssh/config && \
    chown vscode:vscode /home/vscode/.ssh/config

# Add GitHub to known hosts
RUN ssh-keyscan github.com >> /home/vscode/.ssh/known_hosts && \
    chmod 644 /home/vscode/.ssh/known_hosts && \
    chown vscode:vscode /home/vscode/.ssh/known_hosts

# Clone repositories
RUN mkdir -p /workspaces/dev_greenova && \
    git clone -b main git@github.com:enveng-group/dev_greenova.git /workspaces/dev_greenova && \
    chown -R vscode:vscode /workspaces/dev_greenova

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

USER vscode

# Set Git config for dotfiles
RUN git config --global user.name "enveng-group" && \
    git config --global user.email "164126503+enveng-group@users.noreply.github.com"