import serial
import time
import RPi.GPIO as GPIO
# from utils.log import log
# from utils.files import get_configs

GPIO.setmode(GPIO.BOARD)
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)


def send_sms(msg):
    # if get_configs('sms')['send_sms']:
    #     # port.write(b'AT\r')
    #     # rcv = port.read(10)
    #     # print(rcv)
    #     # time.sleep(1)
    #     #
    #     # port.write(b"AT+CMGF=1\r")
    #     #
    #     # # log("Text Mode Enabled…")
    #     # time.sleep(3)
    #     # port.write(bytes('AT+CMGS="{}″\r'.format(get_configs('sms')['target_phone_number']), 'utf-8'))
    #     # # log("sending message….")
    #     # time.sleep(3)
    #     # port.reset_output_buffer()
    #     # time.sleep(1)
    #     # port.write(str.encode(msg+chr(26)))
    #     # time.sleep(3)
    #     # # log("message sent...")
    port.write(b'AT\r')
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)

    port.write(b"AT+CMGF=1\r")

    # log("Text Mode Enabled…")
    time.sleep(3)
    port.write(bytes('AT+CMGS="{}″\r'.format('989129334535'), 'utf-8'))
    # log("sending message….")
    time.sleep(3)
    port.reset_output_buffer()
    time.sleep(1)
    port.write(str.encode(msg + chr(26)))
    time.sleep(3)
    # log("message sent...")


send_sms('test')
