# use Alpine Linux as base image
FROM alpine:3.18

# install system dependencies
RUN apk add --no-cache python3=3.9.21 nodejs=18.20.7 npm=10.8.2 git bash

# set Python 3 as the default Python version
RUN ln -sf /usr/bin/python3 /usr/bin/python

# set the working directory
WORKDIR /workspaces/greenova

# copy requirements.txt file and package.json file
COPY requirements.txt package.json ./

# install Node.js dependencies
RUN npm install

# install Python dependencies
RUN pip install -r requirements.txt -c constraints.txt --no-deps
#RUN pip install --no-cache-dir -r requirements.txt

# set environment variables
ENV PYTHONUNBUFFERED=1

# lunch bash
CMD ["/bin/bash"]
