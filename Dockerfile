FROM balenalib/raspberry-pi-debian:latest

RUN apt-get update && apt-get -y upgrade && apt-get update
RUN apt-get -y install sudo dpkg-dev debhelper dh-virtualenv \
  python3 python3-venv

RUN apt-get -y install libxslt-dev libxml2-dev
RUN apt-get -y install build-essential libssl-dev libffi-dev python3-dev
RUN apt-get -y install zlib1g-dev
RUN bash -c "curl -sSL https://install.python-poetry.org | python3 -"

ENV PATH=$PATH:/root/.local/bin \
  DEB_BUILD_ARCH=armhf \
  DEB_BUILD_ARCH_BITS=32 \
  PIP_DEFAULT_TIMEOUT=600 \
  PIP_TIMEOUT=600 \
  PIP_RETRIES=100

RUN mkdir /build
COPY . /build/

WORKDIR /build
RUN /root/.local/bin/poetry build

WORKDIR /build/dist
RUN dpkg-buildpackage -us -uc
