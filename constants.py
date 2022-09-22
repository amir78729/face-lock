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
    with open('configs.json', 'r') as json_file:
        configs = json.load(json_file)
    return configs[config_key]


def get_username_by_id(_id):
    """
    Getting username by id

    :param _id: user id
    :return: username
    """
    with open(get_configs('names_data'), 'r') as json_file:
        names = json.load(json_file)
    return names[_id]
