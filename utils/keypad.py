from utils.system import is_raspberry
import time
if is_raspberry:
    import RPi.GPIO as GPIO

KEYPAD_INPUTS = {
    '1': '1', '2': '2', '3': '3', 'A': 'A',
    '4': '4', '5': '5', '6': '6', 'B': 'B',
    '7': '7', '8': '8', '9': '9', 'C': 'C',
    '*': '*', '0': '0', '#': '#', 'D': 'D'
}

KEYPAD_VALID_NUMERIC_INPUTS = [KEYPAD_INPUTS['1'], KEYPAD_INPUTS['2'], KEYPAD_INPUTS['3'], KEYPAD_INPUTS['4'],
                               KEYPAD_INPUTS['5'], KEYPAD_INPUTS['6'], KEYPAD_INPUTS['7'], KEYPAD_INPUTS['8'],
                               KEYPAD_INPUTS['9'], KEYPAD_INPUTS['*'], KEYPAD_INPUTS['0'], KEYPAD_INPUTS['#']]
KEYPAD_VALID_COMMAND_INPUTS = [KEYPAD_INPUTS['A'], KEYPAD_INPUTS['B'], KEYPAD_INPUTS['C'], KEYPAD_INPUTS['D']]
KEYPAD_KEYMAP = [
    [KEYPAD_INPUTS['1'], KEYPAD_INPUTS['2'], KEYPAD_INPUTS['3'], KEYPAD_INPUTS['A']],
    [KEYPAD_INPUTS['4'], KEYPAD_INPUTS['5'], KEYPAD_INPUTS['6'], KEYPAD_INPUTS['B']],
    [KEYPAD_INPUTS['7'], KEYPAD_INPUTS['8'], KEYPAD_INPUTS['9'], KEYPAD_INPUTS['C']],
    [KEYPAD_INPUTS['*'], KEYPAD_INPUTS['0'], KEYPAD_INPUTS['#'], KEYPAD_INPUTS['D']],
]

# These are the GPIO pins where the
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
# if is_raspberry:
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BCM)
#
#     GPIO.setup(L1, GPIO.OUT)
#     GPIO.setup(L2, GPIO.OUT)
#     GPIO.setup(L3, GPIO.OUT)
#     GPIO.setup(L4, GPIO.OUT)
#
#     # Use the internal pull-down resistors
#     GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#     GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#     GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#     GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#
# keypadPressed = -1
#
#
# # This callback registers the key that was pressed
# # if no other key is currently pressed
# def keypad_callback(channel):
#     global keypadPressed
#     if keypadPressed == -1:
#         keypadPressed = channel
#
#
# # # Detect the rising edges on the column lines of the
# # # keypad. This way, we can detect if the user presses
# # # a button when we send a pulse.
# if is_raspberry:
#     GPIO.add_event_detect(C1, GPIO.RISING, callback=keypad_callback)
#     GPIO.add_event_detect(C2, GPIO.RISING, callback=keypad_callback)
#     GPIO.add_event_detect(C3, GPIO.RISING, callback=keypad_callback)
#     GPIO.add_event_detect(C4, GPIO.RISING, callback=keypad_callback)
#
#
# def read_keypad_line(line, characters):
#     if is_raspberry:
#         GPIO.output(line, GPIO.HIGH)
#         pressed = ''
#         if GPIO.input(C1) == 1:
#             pressed = characters[0]
#         if GPIO.input(C2) == 1:
#             pressed = characters[1]
#         if GPIO.input(C3) == 1:
#             pressed = characters[2]
#         if GPIO.input(C4) == 1:
#             pressed = characters[3]
#         GPIO.output(line, GPIO.LOW)
#         return pressed
#
#
# def read_keypad():
#     global keypadPressed
#     if is_raspberry:
#         if GPIO.event_detected(C1) or GPIO.event_detected(C2) or GPIO.event_detected(C3) or GPIO.event_detected(C4):
#             key = ''
#             for line, characters in zip([L1, L2, L3, L4], KEYPAD_KEYMAP):
#                 key = read_keypad_line(line, characters)
#                 if key:
#                     break
#             time.sleep(0.1)
#             return key


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

class Keypad:
    # The GPIO pin of the column of the key that is currently
    # being held down or -1 if no key is pressed
    keypad_pressed = -1

    input = ""

    def keypad_callback(self, channel):
        if self.keypad_pressed == -1:
            self.keypad_pressed = channel

    def __init__(self):

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

        # Detect the rising edges on the column lines of the
        # keypad. This way, we can detect if the user presses
        # a button when we send a pulse.
        GPIO.add_event_detect(C1, GPIO.RISING, callback=self.keypad_callback)
        GPIO.add_event_detect(C2, GPIO.RISING, callback=self.keypad_callback)
        GPIO.add_event_detect(C3, GPIO.RISING, callback=self.keypad_callback)
        GPIO.add_event_detect(C4, GPIO.RISING, callback=self.keypad_callback)

    def read_line(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        x = None
        if (GPIO.input(C1) == 1):
            # self.input = self.input + characters[0]
            x = characters[0]
        if (GPIO.input(C2) == 1):
            # self.input = self.input + characters[1]
            x = characters[1]
        if (GPIO.input(C3) == 1):
            # self.input = self.input + characters[2]
            x = characters[2]
        if (GPIO.input(C4) == 1):
            # self.input = self.input + characters[3]
            x = characters[3]
        GPIO.output(line, GPIO.LOW)
        return x

    def get_character(self):
        # for L, buttons in zip([L1, L2, L3, L4], [
        #     ["1", "2", "3", "A"],
        #     ["4", "5", "6", "B"],
        #     ["7", "8", "9", "C"],
        #     ["*", "0", "#", "D"]
        # ]):
        for L, buttons in zip([L1, L2, L3, L4], KEYPAD_KEYMAP):
            i = self.read_line(L, buttons)
            if i:
                return i
        return None
