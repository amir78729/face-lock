import time
from utils.system import is_raspberry

BUZZER_DELAY = 0.3
BUZZER_PIN = 4

if is_raspberry:
    from gpiozero import Buzzer
    from signal import pause

def buzz(n):
    if is_raspberry:
        buzzer = Buzzer(BUZZER_PIN)
        for i in range(n):
            buzzer.on()
            time.sleep(BUZZER_DELAY)
            buzzer.off()
            time.sleep(BUZZER_DELAY)


def buzz_on():
    if is_raspberry:
        buzzer = Buzzer(BUZZER_PIN)
        buzzer.on()
        pause()


def buzz_off():
    if is_raspberry:
        buzzer = Buzzer(BUZZER_PIN)
        buzzer.off()
        time.sleep(BUZZER_DELAY)


