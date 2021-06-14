Software Setup
==============

Once your :doc:`hardware setup <hardware-setup>` done, you will have to:

1. Install the ``mariner3d`` Debian package
2. Setup the `USB Gadget driver
   <https://www.kernel.org/doc/html/latest/driver-api/usb/gadget.html>`_ so that
   the printer can see uploaded files
3. Enable the serial port so the Raspberry Pi can send commands to the printer

This section will guide you through those steps.

Installing package
------------------

First, enable the repository:

.. code-block:: bash

   $ curl -sL gpg.l9o.dev | sudo apt-key add -
   $ echo "deb https://ppa.l9o.dev/raspbian ./" | sudo tee /etc/apt/sources.list.d/l9o.list
   $ sudo apt update

Then install mariner:

.. code-block:: bash

   $ sudo apt install mariner3d

USB Gadget Setup
----------------

In order to make the printer see the files uploaded to mariner, we need to
setup the `USB Gadget driver
<https://www.kernel.org/doc/html/latest/driver-api/usb/gadget.html>`_ as a Mass
Storage device. This section will guide you through that process.

Enable USB driver for gadget modules by adding this line to
``/boot/config.txt``:

If you are using a Pi Zero W or a Pi 4B add:

.. code-block:: bash

   dtoverlay=dwc2
   
If you are using a Pi 3A+, there is a little variant as these supports device
mode or host mode, but not "true" OTG which is auto-sensing between host and
device (AKA gadget). So, for the Pi 3A+ you have to add:

.. code-block:: bash

   dtoverlay=dwc2,dr_mode=peripheral

Enable the dwc2 kernel module, by adding this to your ``/boot/cmdline.txt``
just after ``rootwait``:

.. code-block:: bash

   modules-load=dwc2

Setup a container file for storing uploaded files, the ``count=`` is in MB,
use multiples of 1024 to get the number of GBs you want:

.. code-block:: bash

   $ sudo dd bs=1M if=/dev/zero of=/piusb.bin count=2048
   $ sudo mkdosfs /piusb.bin -F 32 -I

Create the mount point for the container file:

.. code-block:: bash

   $ sudo mkdir -p /mnt/usb_share

Add the following line to your ``/etc/fstab`` so the container file gets
mounted on boot::

   /piusb.bin /mnt/usb_share vfat users,gid=mariner,umask=002 0 2

Finally, make ``/etc/rc.local`` load the ``g_mass_storage`` module. If that file
doesn't exist yet, create it with the following contents:

.. code-block:: sh

   #!/bin/sh -e

   modprobe g_mass_storage file=/piusb.bin stall=0 ro=1

   exit 0

If the file exists, you should simply add the ``modprobe`` line to it.

Once you restart the pi (or potentially run ``sudo mount -a``), the printer
should start seeing the contents of ``/mnt/usb_share``.

Setting up the serial port
--------------------------

First, enable UART by adding this to ``/boot/config.txt``::

   enable_uart=1

In order for the Pi to communicate with the printer's mainboard over
serial, you also need to disable the Pi's console over the serial port:

.. code-block:: bash

   $ sudo systemctl stop serial-getty@ttyS0
   $ sudo systemctl disable serial-getty@ttyS0

Lastly, remove the console from ``cmdline.txt`` by removing this from it::

   console=serial0,115200
