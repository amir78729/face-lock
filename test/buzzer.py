import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

if __name__ == '__main__':
    while True:
        print('locking door...')
        GPIO.output(17, 0)
        time.sleep(1)

        print('unlocking door...')
        GPIO.output(17, 1)
        time.sleep(1)
