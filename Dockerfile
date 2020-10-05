FROM balenalib/raspberry-pi-debian:latest

RUN apt-get update && apt-get -y upgrade && apt-get update
RUN apt-get -y install sudo dpkg-dev debhelper dh-virtualenv \
  python3 python3-venv

RUN apt-get -y install libxslt-dev libxml2-dev
RUN apt-get -y install build-essential libssl-dev libffi-dev python3-dev
RUN apt-get -y install zlib1g-dev
RUN bash -c "curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -"
ENV PATH $PATH:/root/.poetry/bin

RUN mkdir /build
COPY . /build/

ENV DEB_BUILD_ARCH=armhf
ENV DEB_BUILD_ARCH_BITS=32
ENV PIP_DEFAULT_TIMEOUT=600
ENV PIP_TIMEOUT=600
ENV PIP_RETRIES=100

WORKDIR /build
RUN python3 /root/.poetry/bin/poetry build

WORKDIR /build/dist
RUN dpkg-buildpackage -us -uc
