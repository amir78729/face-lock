import time
from utils.system import is_raspberry
from constants.raspberry_pi import BUZZER_PIN, BUZZER_DELAY, HIGH, LOW

if is_raspberry:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)


def buzz_on():
    if is_raspberry:
        GPIO.output(BUZZER_PIN, HIGH)


def buzz_off():
    if is_raspberry:
        GPIO.output(BUZZER_PIN, LOW)


def buzz(n):
    if is_raspberry:
        for i in range(n):
            buzz_on()
            time.sleep(BUZZER_DELAY)
            buzz_off()
            time.sleep(BUZZER_DELAY)
