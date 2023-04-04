import time
from utils.system import is_raspberry

buzzer = None

BUZZER_DELAY = 0.3

if is_raspberry:
    from gpiozero import Buzzer
    buzzer = Buzzer(4)


def buzz(n):
    if is_raspberry:
        for i in range(n):
            buzzer.on()
            time.sleep(BUZZER_DELAY)
            buzzer.off()
            time.sleep(BUZZER_DELAY)

