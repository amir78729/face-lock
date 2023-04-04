import time
from utils.system import is_raspberry

LED_PIN = 2
LED_DELAY = 0.2
HIGH = 1
LOW = 0


if is_raspberry:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
    GPIO.setup(LED_PIN, GPIO.OUT)


def led_on():
    if is_raspberry:
        GPIO.output(LED_PIN, HIGH)


def led_off():
    if is_raspberry:
        GPIO.output(LED_PIN, LOW)




