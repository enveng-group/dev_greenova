#!/bin/ash
# filepath: .devcontainer/local-features/dropbear/install.sh
set -e
apk add --no-cache dropbear dropbear-dbclient dropbear-convert dropbear-ssh dropbear-openrc
