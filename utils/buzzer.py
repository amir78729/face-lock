import time
from utils.system import is_raspberry

BUZZER_DELAY = 0.3

if is_raspberry:
    from gpiozero import Buzzer


def buzz(n):
    if is_raspberry:
        buzzer = Buzzer(4)
        print(buzzer)
        for i in range(n):
            buzzer.on()
            time.sleep(BUZZER_DELAY)
            buzzer.off()
            time.sleep(BUZZER_DELAY)

