# 🛰️ mariner

[![Build Status](https://travis-ci.com/luizribeiro/mariner.svg?branch=master)](https://travis-ci.com/luizribeiro/mariner)
[![codecov](https://codecov.io/gh/luizribeiro/mariner/branch/master/graph/badge.svg)](https://codecov.io/gh/luizribeiro/mariner)
[![Python 3.6 | 3.8](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)](https://www.python.org/downloads/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

Web interface for controlling Elegoo Mars Pro 3D Printers.

![Screenshot](docs/img/screenshot.png)

## Features

* Web interface with support for both desktop and mobile.
* Upload files to be printed through the web UI over WiFi!
* Remotely check print status: progress, current layer, time left.
* Remotely control the printer: start prints, pause/resume and stop.
* Browse files available for printing.
* Inspect `.ctb` files: image preview, print time and slicing settings.
* Only supports the Elegoo Mars Pro printer right now.

## Documentation

[This blog post](https://l9o.dev/posts/controlling-an-elegoo-mars-pro-remotely/)
explains the setup end to end with pictures of the modifications done to
an Elegoo Mars Pro.

Alternatively, the documentation is hosted on this repository itself:

* **[Installing](docs/install.md)**: how to setup mariner on a Raspberry
  Pi Zero W and an Elegoo Mars Pro.
* **[Contributing](docs/contributing.md)**: how to setup your development
  environment and contribute to the project. Pull requests are welcome!
