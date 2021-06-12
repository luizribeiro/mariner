Hardware setup
--------------

These are high level instructions for the hardware setup:

1. Setup a Raspberry Pi Zero W, Pi 4B or Pi 3A+ with ssh access over WiFi
2. Wire it to the serial port on the ChiTu mainboard. Do not connect the 5V
   line unless you want your printer's board to power your Pi (might work with
   Pi Zero W, other boards probably won't)
3. Connect the USB OTG port on the Pi to the USB port of the mainboard. Do
   not connect the 5V line. You can put some tape on the connector to
   isolate the 5V line of the USB cable. If using a Pi 3A+, you will need a USB
   A male to USB A male cable.
4. Connect Pi's USB PWR port to a power supply. You can also use a 12V to 5V
   converter from the printer's power supply. Do not connect if you plan on
   powering from the printer's mainboard.

For more detailed instructions for the Elegoo Mars Pro, refer to `this blog post
<https://l9o.dev/posts/controlling-an-elegoo-mars-pro-remotely/>`_. The setup
for other printers should be almost identical.

Once you have your hardware setup, it's time to :doc:`setup your software
<software-setup>`.
