from utils.system import is_raspberry

LED_PIN = 3

if is_raspberry:
    from gpiozero import LED


def led_on():
    if is_raspberry:
        led = LED(LED_PIN)
        led.on()


def led_off():
    if is_raspberry:
        led = LED(LED_PIN)
        led.off()



