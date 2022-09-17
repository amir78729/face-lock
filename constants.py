import json


ESCAPE = 27
ENTER = 13
TAB = 9
DELETE = 127


def get_configs(config_key):
    config_file = open('configs.json')
    configs = json.load(config_file)
    config_file.close()
    return configs[config_key]
