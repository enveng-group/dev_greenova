#!/bin/ash
# filepath: .devcontainer/local-features/dropbear/install.sh
set -e

# Install Dropbear SSH server and client
apk add --no-cache dropbear dropbear-dbclient dropbear-convert dropbear-ssh dropbear-openrc

# Ensure dropbear client is the default SSH client
ln -sf /usr/bin/dbclient /usr/bin/ssh

# Install Python-based ssh-keygen wrapper for Git compatibility
cp "$(dirname "$0")/ssh-keygen-wrapper.py" /usr/bin/ssh-keygen
chmod +x /usr/bin/ssh-keygen

echo "Dropbear SSH installed with Python ssh-keygen wrapper for Git compatibility"
