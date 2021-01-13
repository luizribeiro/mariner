# Installing

> **Disclaimer:** this software is provided "as is", without warranty of
> any kind. There is no guarantee this will work on your printer, nor
> that it won't damage it. Use at your own risk.

These are really rough installation instructions. I'll write better ones
later:

## Requirements

* Raspberry Pi Zero W
* One of the [supported 3D Printers](https://github.com/luizribeiro/mariner#supported-printers)
* Micro USB to USB-A cable to connect between Pi and printer mainboard.
* Power Supply for the Pi, or a 12V to 5V converter to power it from
  printer's power supply.

## Hardware setup

1. Setup a Raspberry Pi Zero W with ssh access over WiFi.
2. Wire it to the serial port on the Elegoo Mars Pro's mainboard. Do not
   connect the 5V line.
3. Connect the USB OTG port on the Pi to the USB port of the mainboard. Do
   not connect the 5V line. You can put some tape on the connector to
   isolate the 5V line of the USB cable.
4. Connect Pi's USB PWR port to a power supply. You can also use a 12V to 5V
   converter from the printer's power supply.

## Installing package

Download and install the latest release of `mariner3d`:

```
$ wget https://github.com/luizribeiro/mariner/releases/download/v0.1.0-1/mariner3d_0.1.0-1_armhf.deb
$ sudo dpkg -i mariner3d_0.1.0-1_armhf.deb
```

## Allowing printer to see uploaded files

Enable USB driver for gadget modules by adding this line to
`/boot/config.txt`:

```
dtoverlay=dwc2
```

Enable the dwc2 kernel module, by adding this to your `/boot/cmdline.txt`
just after `rootwait`:

```
modules-load=dwc2
```

Setup a container file for storing uploaded files:

```
$ sudo dd bs=1M if=/dev/zero of=/piusb.bin count=2048
$ sudo mkdosfs /piusb.bin -F 32 -I
```

Create the mount point for the container file:

```
$ sudo mkdir -p /mnt/usb_share
```

Add the following line to your `/etc/fstab` so the container file gets
mounted on boot:

```
/piusb.bin /mnt/usb_share vfat users,gid=mariner,umask=002 0 2
```

Finally, make `/etc/rc.local` load the `g_mass_storage` module by adding
this to it:

```sh
#!/bin/sh -e

modprobe g_mass_storage file=/piusb.bin stall=0 ro=1

exit 0
```

Once you restart the pi (or potentially run `sudo mount -a`), the printer
should start seeing the contents of `/mnt/usb_share`.

## Setting up the serial port

First, enable UART by adding this to `/boot/config.txt`:

```
enable_uart=1
```

In order for the Pi to communicate with the printer's mainboard over
serial, you also need to disable the Pi's console over the serial port:

```
$ sudo systemctl stop serial-getty@ttyS0
$ sudo systemctl disable serial-getty@ttyS0
```

Lastly, remove the console from `cmdline.txt` by removing this from it:

```
console=serial0,115200
```

## Wrapping up

Reboot the Pi and you should be all set. Again these are rough
instructions for now :)

You can check that `mariner` is running first by running:

```
$ sudo systemctl status mariner3d
```

If it is, you should be able to access it by opening
`http://<pi ip address>:5000/` on your browser.

