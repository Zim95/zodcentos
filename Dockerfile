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
RUN apt install -y python3.9 python3-pip cmake
RUN apt-get install -y python3.9-dev default-libmysqlclient-dev libpq-dev build-essential

RUN python3.9 -m pip install --no-cache-dir -r requirements.txt
RUN python3.9 -m pip install debugpy
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

ENTRYPOINT [ "python", "app.py" ]