# use Alpine Linux as base image
FROM alpine:3.18

# install system dependencies for pyenv, nvm and compiling python and node
RUN apk add --no-cache \
    bash curl git make gcc g++ \
    linux-headers libc6-compat \
    icu-libs \
    python3 py3-pip python3-dev \
    nodejs npm shellcheck

# set the working directory
WORKDIR /workspaces/greenova

# set Python 3 as the default Python version
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# copy requirements.txt file and package.json file
COPY requirements.txt constraints.txt package.json ./
COPY post_start.sh /usr/local/scripts/post_start.sh
COPY run.sh /usr/local/scripts/run.sh
RUN chmod +x /usr/local/scripts/*.sh

# install Node.js dependencies
#RUN npm install 

# install Python dependencies
#RUN pip install -r requirements.txt -c constraints.txt --no-deps
#RUN pip install --no-cache-dir -r requirements.txt

# add vscode user and group(UID = 1000)
RUN addgroup -g 1000 vscode && \
    adduser -u 1000 -G vscode -s /bin/sh -D vscode && \
    mkdir -p /home/vscode /usr/local /workspaces/greenova && \
    chown -R vscode:vscode /home/vscode /usr/local /workspaces || true

#change user to vscode
USER vscode

# set environment variables
ENV PYTHONUNBUFFERED=1

# lunch bash
CMD ["/bin/bash"]