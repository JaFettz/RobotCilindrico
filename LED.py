import time
from xbox360controller import Xbox360Controller

with Xbox360Controller() as controller:
    controller.set_led(Xbox360Controller.LED_ROTATE)
    time.sleep(1)
    controller.set_led(Xbox360Controller.LED_OFF)
