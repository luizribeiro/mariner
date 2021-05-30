Troubleshooting
===============

Common Issues
-------------

.. rubric:: Slow WiFi

If uploading or accessing mariner is too slow, the following might help:

* If you are powering your Raspberry Pi from a 5V pin on the printer's
  mainboard, try using an external power supply or a buck converter from the
  printer's 12V line. WiFi reception has been reported to be weaker when
  powering the RPi directly from the printer's mainboard.
* `Use an external antenna
  <https://www.briandorey.com/post/raspberry-pi-zero-w-external-antenna-mod>`_.
* Try moving the RPi to outside of the printer case.
* Try moving your RPi closer to your router, `consider using ethernet
  <https://www.raspberrypi-spy.co.uk/2020/05/adding-ethernet-to-a-pi-zero/>`_ or
  a different model such as the RPi 4B, which has onboard ethernet.

.. rubric:: Disk init fail

If your printer is returning an error such as ``//Disk init fail!\r\n``, it
means your Raspberry Pi is not properly configured to use Linux's USB Gadget
mode and your printer is failing to see the virtual disk shared by the RPi.
Please refer to the :ref:`USB Gadget Setup` section of the documentation and
check your setup carefully.

Often, this can be one of these issues:

* **Check for bad USB cables.** Your Micro USB cable should be able to transfer
  data. There are a lot of USB cables out there that don't have the D+/D- data
  lines connected and only have the 5V and GND pins connected. Check that your
  USB cable works with other devices!
* Your ``/etc/rc.local`` isn't setup correctly with the ``modprobe
  g_mass_storage`` line (see `Issue #412
  <https://github.com/luizribeiro/mariner/issues/412>`_ for an example).
* Make sure ``dtoverlay=dwc2`` is under the ``[all]`` section of your
  ``/boot/config.txt``.
* Make sure your Raspberry Pi `supports USB OTG
  <https://en.wikipedia.org/wiki/Raspberry_Pi#Specifications>`_.


.. rubric:: Unexpected Printer Response

If you are seeing the "Unexpected Printer Response" while printing from the web
interface (but printing is working fine), then you are running into `Issue #180
<https://github.com/luizribeiro/mariner/issues/180>`_, which is being worked on.

This has no performance effect and won't cause issues with your prints. It
should cause nothing but cosmetic issues on the user interface and can safely
be ignored. Just refresh the page if you run into it.

.. rubric:: No such file or directory: /dev/serial0

If you are seeing this on the logs for the ``mariner3d`` service on
``journalctl``, this means your serial port is not setup properly. Please refer
to the :ref:`Setting up the serial port` section of the installation guide.

.. rubric:: Error: File is not existed or empty

If your printer is returning responses such as ``Error: File is not existed or
empty``, make sure to upgrade to the latest version of mariner. This is an old
issue which was fixed on ``v0.2.0``. See `Issue #311
<https://github.com/luizribeiro/mariner/issues/311>`_.

.. rubric:: Printer stops during print

If your printer is stopping during the print process, make sure to upgrade to
the latest version of mariner. This is an old issue which was fixed on
``v0.2.0``. See `Issue #311
<https://github.com/luizribeiro/mariner/issues/311>`_.

Other Issues
------------

If your issue isn't listed above, check the ``mariner3d`` logs for clues:

.. code-block:: bash

   $ sudo journalctl -ub mariner3d.service

Also check the message buffer of the Linux kernel for errors:

.. code-block:: bash

   $ sudo dmesg

Carefully read the :ref:`Installation Guide` once again and, if none of that
helps, `file an issue on GitHub
<https://github.com/luizribeiro/mariner/issues/new/choose>`_!
