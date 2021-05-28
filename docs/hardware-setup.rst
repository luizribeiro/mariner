Hardware setup
--------------

These are high level instructions for the hardware setup:

1. Setup a Raspberry Pi Zero W with ssh access over WiFi.
2. Wire it to the serial port on the ChiTu mainboard. Do not connect the 5V
   line.
3. Connect the USB OTG port on the Pi to the USB port of the mainboard. Do
   not connect the 5V line. You can put some tape on the connector to
   isolate the 5V line of the USB cable.
4. Connect Pi's USB PWR port to a power supply. You can also use a 12V to 5V
   converter from the printer's power supply.

For more detailed instructions for the Elegoo Mars Pro, refer to `this blog post
<https://l9o.dev/posts/controlling-an-elegoo-mars-pro-remotely/>`_. The setup
for other printers should be almost identical.

Once you have your hardware setup, it's time to :doc:`setup your software
<software-setup>`.
