import serial
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

port.write(b'AT\r\n')
rcv = port.read(10)
print(rcv)
time.sleep(1)

port.write(b'ATE0\r\n')  # Disable the Echo
rcv = port.read(10)
print(rcv)
time.sleep(1)

port.write(b'AT+CMGF=1\r\n')  # Select Message format as Text mode 
rcv = port.read(10)

print(rcv)
time.sleep(1)

port.write(b'AT+CNMI=2,1,0,0,0\r\n')  # New SMS Message Indications
rcv = port.read(10)

print(rcv)
time.sleep(1)

# Sending a message to a particular Number

port.write(b'AT+CMGS="989129334535"\r\n')
rcv = port.read(10)

print(rcv)
time.sleep(1)

port.write(b'Hello User\r\n')  # Message
rcv = port.read(10)

print(rcv)

port.write(b'\x1A')  # Enable to send SMS
for i in range(10):
    rcv = port.read(10)
    print(rcv)
