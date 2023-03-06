import RPi.GPIO as GPIO
import time

KEYPAD_VALID_NUMERIC_INPUTS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']
KEYPAD_VALID_COMMAND_INPUTS = ['A', 'B', 'C', 'D']

_input=""

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

keypadPressed = -1


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
        if _input == '1234':
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
        print(characters[0])
        _input = _input + characters[0]
    if GPIO.input(C2) == 1:
        print(characters[1])
        _input = _input + characters[1]
    if GPIO.input(C3) == 1:
        print(characters[2])
        _input = _input + characters[2]
    if GPIO.input(C4) == 1:
        print(characters[3])
        _input = _input + characters[3]
    GPIO.output(line, GPIO.LOW)
    print(_input)


try:
    while True:
        # If a button was previously pressed,
        # check, whether the user has released it yet
        if keypadPressed != -1:
            set_all_lines(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                time.sleep(0.3)
        # Otherwise, just read the _input
        else:
            if not check_special_keys():
                read_line(L1, ["1", "2", "3", "A"])
                read_line(L2, ["4", "5", "6", "B"])
                read_line(L3, ["7", "8", "9", "C"])
                read_line(L4, ["*", "0", "#", "D"])
                time.sleep(0.3)
            else:
                time.sleep(0.3)
except KeyboardInterrupt:
    print("\nApplication stopped!")


MOBILE_NUMERIC_KEYPAD_DICTIONARY = {
    '0': '0',
    ' ': '',
    '1': '1',
    '2': '2222',
    '3': '3333',
    '4': '4444',
    '5': '5555',
    '6': '6666',
    '7': '77777',
    '8': '8888',
    '9': '99999',
    'a': '2',
    'b': '22',
    'c': '222',
    'd': '3',
    'e': '33',
    'f': '333',
    'g': '4',
    'h': '44',
    'i': '444',
    'j': '5',
    'k': '55',
    'l': '555',
    'm': '6',
    'n': '66',
    'o': '666',
    'p': '7',
    'q': '77',
    'r': '777',
    's': '7777',
    't': '8',
    'u': '88',
    'v': '888',
    'w': '9',
    'x': '99',
    'y': '999',
    'z': '9999',
}


def get_char_from_numeric_sequence(_numeric_sequence):
    return [k for k, v in MOBILE_NUMERIC_KEYPAD_DICTIONARY.items() if v == _numeric_sequence][0]


def get_numeric_sequence_from_char(_char):
    return MOBILE_NUMERIC_KEYPAD_DICTIONARY[_char]


def convert_keypad_input_sequence_to_string(input_string):
    result = ''
    for x in input_string.split('#'):
        try:
            result += get_char_from_numeric_sequence(x)
        except IndexError:
            for i in range(len(x) - 1):
                try:
                    result += get_char_from_numeric_sequence(x[i + 1:]) + get_char_from_numeric_sequence(x[:i + 1])
                    break
                except IndexError:
                    pass
    return result


def standardize_keypad_input_sequence(input_string):
    result = ''
    if input_string != '':
        for i in range(len(input_string) - 1):
            result += input_string[i]
            if not input_string[i] == input_string[i + 1] and '#' not in [input_string[i], input_string[i + 1]]:
                result += '#'
            if input_string[i] == '#' and \
                    input_string[i - 1] != input_string[i + 1] and \
                    '#' not in [input_string[i - 1], input_string[i + 1]]:
                result += '#'
        result += input_string[-1]
    return result
