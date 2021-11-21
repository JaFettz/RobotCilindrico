from xbox360controller import Xbox360Controller

with Xbox360Controller() as controller:
    controller.set_rumble(0.5, 0.5, 1000)
    time.sleep(0.5)
