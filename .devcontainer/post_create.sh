#!/bin/sh

set -e

# Check if directories exist before changing ownership
if [ -d "/home/vscode/.ssh" ]; then
    if ! chown -R vscode:vscode /home/vscode/.ssh; then
        echo "Error: Failed to set ownership of .ssh directory" >&2
        exit 1
    fi
fi

# Set proper permissions for .ssh directory
if [ -d "/home/vscode/.ssh" ]; then
    if ! chmod 700 /home/vscode/.ssh; then
        echo "Error: Failed to set permissions on .ssh directory" >&2
        exit 1
    fi

    # Set proper permissions for SSH key if they exist
    if [ -f "/home/vscode/.ssh/id_ed25519" ]; then
        if ! chmod 600 /home/vscode/.ssh/id_ed25519; then
            echo "Error: Failed to set permissions on SSH private key" >&2
            exit 1
        fi
    fi

        # Set proper permissions for public SSH key if they exist
    if [ -f "/home/vscode/.ssh/id_ed25519.pub" ]; then
        if ! chmod 644 /home/vscode/.ssh/id_ed25519.pub; then
            echo "Error: Failed to set permissions on SSH public key" >&2
            exit 1
        fi
    fi
fi

exit 0
