# This program allows a user to enter a
# Code. If the C-Button is pressed on the
# keypad, the _input is reset. If the user
# hits the A-Button, the _input is checked.

import RPi.GPIO as GPIO
import time

# These are the GPIO pin numbers where the
# lines of the keypad matrix are connected
L1 = 5
L2 = 6
L3 = 13
L4 = 19

# These are the four columns
C1 = 12
C2 = 16
C3 = 20
C4 = 21

# The GPIO pin of the column of the key that is currently
# being held down or -1 if no key is pressed
keypadPressed = -1

secretCode = "4789"
_input = ""

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# This callback registers the key that was pressed
# if no other key is currently pressed
def keypad_callback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel


# Detect the rising edges on the column lines of the
# keypad. This way, we can detect if the user presses
# a button when we send a pulse.
GPIO.add_event_detect(C1, GPIO.RISING, callback=keypad_callback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypad_callback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypad_callback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypad_callback)


# Sets all lines to a specific state. This is a helper
# for detecting when the user releases a button
def set_all_lines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)


def check_special_keys():
    global _input
    pressed = False

    GPIO.output(L3, GPIO.HIGH)

    if GPIO.input(C4) == 1:
        print("_input reset!")
        pressed = True

    GPIO.output(L3, GPIO.LOW)
    GPIO.output(L1, GPIO.HIGH)

    if not pressed and GPIO.input(C4) == 1:
        if _input == secretCode:
            print("Code correct!")
            # TODO: Unlock a door, turn a light on, etc.
        else:
            print("Incorrect code!")
            # TODO: Sound an alarm, send an email, etc.
        pressed = True

    GPIO.output(L3, GPIO.LOW)

    if pressed:
        _input = ""

    return pressed


# reads the columns and appends the value, that corresponds
# to the button, to a variable
def read_line(line, characters):
    global _input
    # We have to send a pulse on each line to
    # detect button presses
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(C1) == 1:
        _input = _input + characters[0]
    if GPIO.input(C2) == 1:
        _input = _input + characters[1]
    if GPIO.input(C3) == 1:
        _input = _input + characters[2]
    if GPIO.input(C4) == 1:
        _input = _input + characters[3]
    GPIO.output(line, GPIO.LOW)


try:
    while True:
        # If a button was previously pressed,
        # check, whether the user has released it yet
        if keypadPressed != -1:
            set_all_lines(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                time.sleep(0.1)
        # Otherwise, just read the _input
        else:
            if not check_special_keys():
                read_line(L1, ["1", "2", "3", "A"])
                read_line(L2, ["4", "5", "6", "B"])
                read_line(L3, ["7", "8", "9", "C"])
                read_line(L4, ["*", "0", "#", "D"])
                time.sleep(0.1)
            else:
                time.sleep(0.1)
except KeyboardInterrupt:
    print("\nApplication stopped!")
