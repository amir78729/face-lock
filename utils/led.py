from utils.system import is_raspberry
from constants.raspberry_pi import LED_PIN, HIGH, LOW


if is_raspberry:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)


def led_on():
    if is_raspberry:
        GPIO.output(LED_PIN, HIGH)


def led_off():
    if is_raspberry:
        GPIO.output(LED_PIN, LOW)
