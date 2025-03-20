# use Alpine Linux as base image
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

# set the working directory
WORKDIR /workspaces/greenova

# copy requirements.txt file and package.json file
COPY requirements.txt package.json ./

# install Node.js dependencies
#RUN npm install

# install Python dependencies
RUN pip install -r requirements.txt -c constraints.txt --no-deps
#RUN pip install --no-cache-dir -r requirements.txt

# set environment variables
ENV PYTHONUNBUFFERED=1

# lunch bash
CMD ["/bin/bash"]
