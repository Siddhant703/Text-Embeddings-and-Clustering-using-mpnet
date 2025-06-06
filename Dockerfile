# FROM python:3.7
FROM ubuntu:18.04

# Upgrade installed packages
RUN apt-get update && apt-get upgrade -y && apt clean

# install python 3.7.10 (or newer)
RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get install --no-install-recommends -y git python3.7 python3.7-dev python3.7-distutils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

#Install Curl
RUN apt-get update && apt-get install --no-install-recommends -y curl
# Register the version in alternatives (and set higher priority to 3.7)
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2

# Upgrade pip to latest version
RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py --force-reinstall && \
    rm get-pip.py

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . /app
RUN pip3 install -r requirements.txt

EXPOSE 8080
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080"]