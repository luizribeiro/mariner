🛰️ mariner
==========

|CI| |docs| |codecov| |Python| |MIT license|

Web interface for controlling MSLA 3D Printers based on ChiTu controllers
remotely.

|Screenshot|

Features
--------

- Web interface with support for both desktop and mobile.
- Upload files to be printed through the web UI over WiFi!
- Remotely check print status: progress, current layer, time left.
- Remotely control the printer: start prints, pause/resume and stop.
- Browse files available for printing.
- Inspect ``.ctb`` files: image preview, print time and slicing settings.

For more details on the feature set, refer to our `Documentation
<https://mariner.readthedocs.io/en/latest/>`_.

Supported Printers
------------------

Mariner supports a wide range of MSLA printers, including printers from the
following manufacturers:

- Anycubic
- Creality
- EPAX
- Elegoo
- Peopoly
- Phrozen
- Voxelab

Please refer to the list of `Supported Printers
<https://mariner.readthedocs.io/en/latest/supported-printers.html>`_
on our documentation for a full list of printer models that have been tested.
If you have access to other printers and want to contribute, please open an
issue.  We're happy to support more printers!

Documentation
-------------

The documentation is available from `Read the Docs
<https://mariner.readthedocs.io/en/latest/>`_. It contains a lot of information
from how to setup the hardware, install the software, troubleshoot issues, and
how to contribute to development.

`This blog
post <https://l9o.dev/posts/controlling-an-elegoo-mars-pro-remotely/>`__
explains the setup end to end with pictures of the modifications done to an
Elegoo Mars Pro.

.. |CI| image:: https://github.com/luizribeiro/mariner/workflows/CI/badge.svg
   :target: https://github.com/luizribeiro/mariner/actions/workflows/ci.yaml
.. |docs| image:: https://readthedocs.org/projects/mariner/badge/?version=latest
   :target: https://mariner.readthedocs.io/en/latest/?badge=latest
.. |codecov| image:: https://codecov.io/gh/luizribeiro/mariner/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/luizribeiro/mariner
.. |Python| image:: https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue
   :target: https://www.python.org/downloads/
.. |MIT license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://luizribeiro.mit-license.org/
.. |Screenshot| image:: /docs/_static/screenshot.png
