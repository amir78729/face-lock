KEYPAD_VALID_NUMERIC_INPUTS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']
KEYPAD_VALID_COMMAND_INPUTS = ['A', 'B', 'C', 'D']


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
