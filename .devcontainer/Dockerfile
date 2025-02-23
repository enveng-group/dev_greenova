FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Modified user setup to handle existing user/group
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Only create group and user if they don't exist
RUN if ! getent group $USER_GID > /dev/null 2>&1; then \
        groupadd --gid $USER_GID $USERNAME; \
    fi && \
    if ! getent passwd $USER_UID > /dev/null 2>&1; then \
        useradd --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi && \
    mkdir -p /home/$USERNAME/.ssh && \
    chown -R $USERNAME:$USERNAME /home/$USERNAME/.ssh && \
    chmod 700 /home/$USERNAME/.ssh

# Install build essentials and shell tools
RUN apt-get update && apt-get install -y \
    build-essential \
    shellcheck \
    shfmt \
    openssh-client \
    git

# Install Python build dependencies
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev

# Download and install Python from source
ARG PYTHON_VERSION=3.13.2
RUN cd /tmp && \
    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz && \
    tar -xf Python-${PYTHON_VERSION}.tar.xz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make -j $(nproc) && \
    make altinstall && \
    cd .. && \
    rm -rf Python-${PYTHON_VERSION}* && \
    ln -s /usr/local/bin/python${PYTHON_VERSION%.*} /usr/local/bin/python3 && \
    ln -s /usr/local/bin/pip${PYTHON_VERSION%.*} /usr/local/bin/pip3

# Verify Python installation
RUN python3 --version && \
    pip3 --version

# Install Git from source
ARG GIT_VERSION=2.48.1
RUN apt-get update && apt-get install -y \
    dh-autoreconf \
    libcurl4-gnutls-dev \
    libexpat1-dev \
    gettext \
    libz-dev \
    libssl-dev \
    asciidoc \
    xmlto \
    docbook2x \
    make \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && cd /tmp \
    && wget https://www.kernel.org/pub/software/scm/git/git-${GIT_VERSION}.tar.xz \
    && tar xf git-${GIT_VERSION}.tar.xz \
    && cd git-${GIT_VERSION} \
    && make prefix=/usr/local all \
    && make prefix=/usr/local install \
    && cd .. \
    && rm -rf git-${GIT_VERSION}*

# Install Node.js via nvm
ARG NODE_VERSION=23.8.0
ARG NVM_VERSION=0.40.1
ARG PNPM_VERSION=10.4.1
ENV NVM_DIR=/usr/local/share/nvm

# Create nvm directory and set permissions
RUN mkdir -p $NVM_DIR && \
    chmod -R 777 $NVM_DIR && \
    # Download and install nvm
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v${NVM_VERSION}/install.sh | bash && \
    . $NVM_DIR/nvm.sh && \
    # Install Node.js
    nvm install ${NODE_VERSION} && \
    nvm alias default ${NODE_VERSION} && \
    # Add NVM to PATH and environment
    echo "export NVM_DIR=\"$NVM_DIR\"" >> /etc/bash.bashrc && \
    echo "[ -s \"$NVM_DIR/nvm.sh\" ] && \. \"$NVM_DIR/nvm.sh\"" >> /etc/bash.bashrc && \
    echo "[ -s \"$NVM_DIR/bash_completion\" ] && \. \"$NVM_DIR/bash_completion\"" >> /etc/bash.bashrc && \
    # Install pnpm
    npm install -g pnpm@${PNPM_VERSION}

# Verify installations
RUN . $NVM_DIR/nvm.sh && \
    node --version && \
    npm --version && \
    pnpm --version

# Create scripts directory
RUN mkdir -p /workspaces/scripts && \
    chown -R vscode:vscode /workspaces/scripts

USER vscode

# Initialize workspace
WORKDIR /workspaces
RUN mkdir -p logs && \
    chmod +x scripts/*.sh 2>/dev/null || true

# Set up SSH and Git
RUN mkdir -p /var/lib/apt/lists/partial && \
    chmod 755 /var/lib/apt/lists/partial && \
    apt-get update && apt-get install -y \
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

# Set Git config for dotfiles
RUN git config --global user.name "enveng-group" && \
    git config --global user.email "164126503+enveng-group@users.noreply.github.com"

# Set up workspace for shell script
COPY make.sh /workspaces/
RUN chmod +x /workspaces/make.sh && \
    chown vscode:vscode /workspaces/make.sh