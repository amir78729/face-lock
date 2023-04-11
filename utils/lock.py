from utils.system import is_raspberry
from constants.raspberry_pi import LOCK_PIN, HIGH, LOW


if is_raspberry:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LOCK_PIN, GPIO.OUT)


def close_door():
    if is_raspberry:
        GPIO.output(LOCK_PIN, LOW)


def open_door():
    if is_raspberry:
        GPIO.output(LOCK_PIN, HIGH)
