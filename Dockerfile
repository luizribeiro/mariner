FROM balenalib/raspberry-pi-debian:latest

RUN apt-get update && apt-get -y upgrade && apt-get update
RUN apt-get -y install sudo dpkg-dev debhelper dh-virtualenv \
  python3 python3-venv

RUN apt-get -y install libxslt-dev libxml2-dev
RUN apt-get -y install build-essential libssl-dev libffi-dev python3-dev
RUN apt-get -y install zlib1g-dev

RUN mkdir /build
COPY . /build/
WORKDIR /build

ENV DEB_BUILD_ARCH=armhf
ENV DEB_BUILD_ARCH_BITS=32

RUN dpkg-buildpackage -us -uc
