from utils.system import is_raspberry

LED_PIN = 3

if is_raspberry:
    from gpiozero import Buzzer  # TODO: FIX!
    # from gpiozero import LED


def led_on():
    if is_raspberry:
        led = Buzzer(LED_PIN)  # TODO: FIX!
        led.on()


def led_off():
    if is_raspberry:
        led = Buzzer(LED_PIN)  # TODO: FIX!
        led.off()



