import time
from utils.system import is_raspberry

BUZZER_DELAY = 0.3
BUZZER_PIN = 4

theBuzzer = None
if is_raspberry:
    from gpiozero import Buzzer
    theBuzzer = Buzzer(BUZZER_PIN)


def buzz(n):
    global theBuzzer
    if is_raspberry:
        # buzzer = Buzzer(BUZZER_PIN)
        for i in range(n):
            # buzzer.on()
            theBuzzer.on()
            time.sleep(BUZZER_DELAY)
            # buzzer.off()
            theBuzzer.off()
            time.sleep(BUZZER_DELAY)


def buzz_on():
    global theBuzzer
    if is_raspberry:
        # buzzer = Buzzer(BUZZER_PIN)
        # buzzer.on()
        theBuzzer.on()


def buzz_off():
    global theBuzzer
    if is_raspberry:
        # buzzer = Buzzer(BUZZER_PIN)
        # buzzer.off()
        theBuzzer.off()

