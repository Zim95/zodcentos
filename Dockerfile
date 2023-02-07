FROM ubuntu:20.04

# Directory
RUN mkdir /app
COPY . app
WORKDIR /app

# Pre-setup for Python
RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
RUN apt update && \
    apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa

# Python installation
RUN apt install -y python3.9 python3-pip
RUN apt-get install -y python3.9-dev build-essential
# Installation of requirements.txt
RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Now we will install docker inside the container.
# These installations are from the official documentation.
RUN apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN chmod a+r /etc/apt/keyrings/docker.gpg
RUN apt update
RUN apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# This will install docker and /var/run/docker.sock. If we try to run dockerd inside the container, we will get an error.
# Yhe next step is to map the volume of docker.sock from host machine to the container's docker.sock.
# However we will do this externally while running the container. We will also use volumes in docker-compose later on.

ENTRYPOINT [ "python3.9", "app.py" ]