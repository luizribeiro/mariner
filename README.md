# 🛰️ mariner

![CI](https://github.com/luizribeiro/mariner/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/luizribeiro/mariner/branch/master/graph/badge.svg)](https://codecov.io/gh/luizribeiro/mariner)
[![Python 3.6 | 3.8](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)](https://www.python.org/downloads/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

Web interface for controlling MSLA 3D Printers based on Chitu controllers,
such as the ones by Elegoo and Phrozen.

![Screenshot](docs/img/screenshot.png)

## Features

* Web interface with support for both desktop and mobile.
* Upload files to be printed through the web UI over WiFi!
* Remotely check print status: progress, current layer, time left.
* Remotely control the printer: start prints, pause/resume and stop.
* Browse files available for printing.
* Inspect `.ctb` files: image preview, print time and slicing settings.

## Supported Printers

The following printers have been tested by the community and work with
Mariner:

* Elegoo Mars
* Elegoo Mars Pro
* Elegoo Mars 2 Pro
* Phrozen Sonic Mini 4K
* Creality LD-002H

If you have access to other models and want to contribute, please open an
issue. We're happy to support more printers!

## Documentation

[This blog post](https://l9o.dev/posts/controlling-an-elegoo-mars-pro-remotely/)
explains the setup end to end with pictures of the modifications done to
an Elegoo Mars Pro.

Alternatively, the documentation is hosted on this repository itself:

* **[Installing](docs/install.md)**: how to setup mariner on a Raspberry
  Pi Zero W and an Elegoo Mars Pro. These same instructions have been
  confirmed to work with the printers listed on the section above.
* **[Contributing](docs/contributing.md)**: how to setup your development
  environment and contribute to the project. Pull requests are welcome!
