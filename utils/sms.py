from utils.files import get_configs
from utils.system import is_raspberry
from utils.log import log
from constants.raspberry_pi import ENCODING, SERIAL_PORT
import serial

if is_raspberry:
    import RPi.GPIO as GPIO


def send_sms(text):
    if is_raspberry and get_configs('sms')['send_sms']:
        try:
            phone_number = get_configs('sms')['phone_number']
            ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=5)
            GPIO.setmode(GPIO.BOARD)
            ser.write(b"AT+CMGF=1\r")  # Text Mode Enabled
            ser.write('AT+CMGS="{}"\r'.format(phone_number).encode(ENCODING))
            ser.reset_output_buffer()
            ser.write('{}'.format(text + chr(26)).encode(ENCODING))  # send sms
            log('send "{}" to {}'.format(text, phone_number))
        except:
            pass
