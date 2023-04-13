import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LOCK_PIN, GPIO.OUT)

if __name__ == '__main__':
    lock = 0
    while True:
        if lock == 0:
            lock = 1
            print('locking door...')
            GPIO.output(24, lock)
            time.sleep(1)
        else:
            lock = 0
            print('unlocking door...')
            GPIO.output(24, lock)
            time.sleep(1)
