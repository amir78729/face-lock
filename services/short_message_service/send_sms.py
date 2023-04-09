# import serial
# import time
# from utils.system import is_raspberry
# # from utils.log import log
# # from utils.files import get_configs
#
# if is_raspberry:
#     import RPi.GPIO as GPIO
#     GPIO.setmode(GPIO.BOARD)
#     ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
#
#
# def send_sms(msg):
#     # if get_configs('sms')['send_sms']:
#     #     # ser.write(b'AT\r')
#     #     # rcv = ser.read(10)
#     #     # print(rcv)
#     #     # time.sleep(1)
#     #     #
#     #     # ser.write(b"AT+CMGF=1\r")
#     #     #
#     #     # # log("Text Mode Enabled…")
#     #     # time.sleep(3)
#     #     # ser.write(bytes('AT+CMGS="{}″\r'.format(get_configs('sms')['target_phone_number']), 'utf-8'))
#     #     # # log("sending message….")
#     #     # time.sleep(3)
#     #     # ser.reset_output_buffer()
#     #     # time.sleep(1)
#     #     # ser.write(str.encode(msg+chr(26)))
#     #     # time.sleep(3)
#     #     # # log("message sent...")
#     ser.write(b'AT\r')
#     rcv = ser.read(10)
#     print(rcv)
#     time.sleep(1)
#
#     ser.write(b"AT+CMGF=1\r")
#
#     print("Text Mode Enabled…")
#     time.sleep(3)
#     ser.write(bytes('AT+CMGS="{}″\r'.format('989121580288'), 'utf-8'))
#     print("sending message….")
#     time.sleep(3)
#     ser.reset_output_buffer()
#     time.sleep(1)
#     ser.write(str.encode(msg + chr(26)))
#     time.sleep(3)
#     print("message sent...")
#
#
# send_sms('test')

# if is_raspberry:
import RPi.GPIO as GPIO
import serial
import time, sys
import datetime

P_BUTTON = 24  # Button, adapt to your wiring


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_BUTTON, GPIO.IN, GPIO.PUD_UP)


SERIAL_PORT = "/dev/ttyAMA0"  # Raspberry Pi 2
# SERIAL_PORT = "/dev/ttyS0"    # Raspberry Pi 3

ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=5)
GPIO.setmode(GPIO.BOARD)

# ser.write(b'AT\r')
# rcv = ser.read(10)
# print(rcv)
# time.sleep(1)
# 
# ser.write(b'ATD9129334535;\r')
# print("Calling…")
# time.sleep(30)
# ser.write(b'ATH\r')
# print("Hang Call…")


ser.write(b"AT+CMGF=1\r")
print("Text Mode Enabled…")
time.sleep(3)
ser.write(b'AT+CMGS="+989129334535"\r')
msg = "test message from SIM900A…"
print("sending message….")
time.sleep(3)
ser.reset_output_buffer()
time.sleep(1)
ser.write(str.encode(msg+chr(26)))
time.sleep(3)
print("message sent…")


# ser.write(b"AT+CMGF=1\r")  # set to text mode
# time.sleep(3)
# ser.write(b'AT+CMGDA="DEL ALL"\r')  # delete all SMS
# time.sleep(3)
# reply = ser.read(ser.inWaiting())  # Clean buf
#
# print('send')
# ser.write(b'AT+CMGS="+989129334535"\r')
# time.sleep(3)
# msg = "test".encode('utf-8')
# ser.write(msg)
# time.sleep(3)
# ser.write(b'AT+CMGDA="DEL ALL"\r')  # delete all
# time.sleep(3)
# ser.read(ser.inWaiting())  # Clear buf
#
# print("Listening for incomming SMS...")
# while True:
#     print('.')
#     reply = ser.read(10)
#     # reply = ser.read(ser.inWaiting())
#     reply = reply.decode("utf-8")
#     print(reply)
#
#     if reply != "":
#         ser.write(b"AT+CMGR=1\r")
#         time.sleep(3)
#         reply = ser.read(10)
#         # reply = ser.read(ser.inWaiting())
#         print("SMS received. Content:")
#         print(reply)
#         if "getStatus" in reply:
#             t = str(datetime.datetime.now())
#             ser.write(b'AT+CMGS="+989129334535"\r')
#             time.sleep(3)
#             msg = "Sending status at " + t + ":--" + 'sss'
#             print("Sending SMS with status info:" + msg)
#             ser.write(msg + chr(26))
#         time.sleep(3)
#         ser.write(b'AT+CMGDA="DEL ALL"\r')  # delete all
#         time.sleep(3)
#         ser.read(ser.inWaiting())  # Clear buf
#     time.sleep(5)
#     # try:
#     #     print('.', end='')
#     #     reply = ser.read(ser.inWaiting())
#     #     reply = reply.decode("utf-8")
#     #     if reply != "":
#     #         ser.write(b"AT+CMGR=1\r")
#     #         time.sleep(3)
#     #         reply = ser.read(ser.inWaiting())
#     #         print("SMS received. Content:")
#     #         print(reply)
#     #         if "getStatus" in reply:
#     #             t = str(datetime.datetime.now())
#     #             if GPIO.input(P_BUTTON) == GPIO.HIGH:
#     #                 state = "Button released"
#     #             else:
#     #                 state = "Button pressed"
#     #             ser.write(b'AT+CMGS="+989129334535"\r')
#     #             time.sleep(3)
#     #             msg = "Sending status at " + t + ":--" + state
#     #             print("Sending SMS with status info:" + msg)
#     #             ser.write(msg + chr(26))
#     #         time.sleep(3)
#     #         ser.write(b'AT+CMGDA="DEL ALL"\r')  # delete all
#     #         time.sleep(3)
#     #         ser.read(ser.inWaiting())  # Clear buf
#     #     time.sleep(5)
#     # except Exception as e:
#     #     print('errrr')
#     #     print(e)
