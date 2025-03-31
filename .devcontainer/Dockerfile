# use Alpine Linux as base image
<<<<<<< HEAD
FROM python:3.9.21-alpine

# install system dependencies for pyenv, nvm and compiling python and node
RUN apk add --no-cache python3 py3-pip python3-dev \
    bash curl fish make shellcheck\
    gcc musl-dev linux-headers git direnv

# install node
RUN curl -fsSL https://unofficial-builds.nodejs.org/download/release/v18.20.7/node-v18.20.7-linux-x64-musl.tar.gz \
    | tar -xz -C /usr/local --strip-components=1 --no-same-owner \
    && ln -s /usr/local/bin/node /usr/bin/node \
    && ln -s /usr/local/bin/npm /usr/bin/npm

# upgrade npm to v10.8.2
RUN npm install -g npm@10.8.2

# verify
RUN node -v && npm -v
=======
FROM alpine:3.18

# install system dependencies
RUN apk add --no-cache python3=3.9.21 nodejs=18.20.7 npm=10.8.2 git bash

# set Python 3 as the default Python version
RUN ln -sf /usr/bin/python3 /usr/bin/python
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

# set the working directory
WORKDIR /workspaces/greenova

<<<<<<< HEAD
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

=======
# copy requirements.txt file and package.json file
COPY requirements.txt package.json ./

# install Node.js dependencies
RUN npm install 

# install Python dependencies
RUN pip install -r requirements.txt -c constraints.txt --no-deps
#RUN pip install --no-cache-dir -r requirements.txt

>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
# set environment variables
ENV PYTHONUNBUFFERED=1

# lunch bash
<<<<<<< HEAD
CMD ["/bin/bash"]
=======
CMD ["/bin/bash"]
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
