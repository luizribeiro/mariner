Requirements
============

Before you get started, make sure you have the following:

* **Raspberry Pi Zero W, Zero WH, 3A+ or 4B**. See Wikipedia's article about the `Raspberry Pi specifications <https://en.wikipedia.org/wiki/Raspberry_Pi#Specifications>`_ for a list of which models support USB OTG.
* **A supported printer.** Most MSLA 3D printers with a ChiTu board should work. We keep a list of `tested 3D Printers <supported-printers.rst>`_ on our documentation.
* **A USB cable** to connect between Pi and printer mainboard, please use:

  * Micro-USB to USB-A male *if using a Pi Zero W*
  * USB-C to USB-A male *if using a Pi 4B*
  * USB-A male to USB-A male *if using a Pi 3A+*

* **Power Supply for the Pi**, or a 12V to 5V converter to power it from
  printer's power supply. Some users have also have had success with using 5V
  pins from the printer mainboard itself. However, that sometimes creates issues
  with poor WiFi signal, making uploading files too slow or it can also cause serial connection drops.
* **Micro-SD card** faster is better and size is depending on how much space you want to have for the printed files. 2GB would likely work but 4GB or 8GB would probably me a better start.
* **An hour or two** and some basic linux knowledge :-)
