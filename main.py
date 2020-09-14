from mariner.mars import ElegooMars


elegoo_mars = ElegooMars()
elegoo_mars.open()
print(f"Firmware Version: {elegoo_mars.get_firmware_version()}")
print(f"State: {elegoo_mars.get_state()}")
elegoo_mars.close()
