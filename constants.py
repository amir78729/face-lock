import json


ESCAPE = 27
ENTER = 13
TAB = 9
DELETE = 127


def get_configs(config_key):
    """
    Getting App Config from ``constants.py``

    :param config_key: Key of desired config
    :return: value of desired config
    """
    config_file = open('configs.json')
    configs = json.load(config_file)
    config_file.close()
    return configs[config_key]


mobile_numeric_keypad_dictionary = {
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
    return [k for k, v in mobile_numeric_keypad_dictionary.items() if v == _numeric_sequence][0]


def get_numeric_sequence_from_char(_char):
    return mobile_numeric_keypad_dictionary[_char]
