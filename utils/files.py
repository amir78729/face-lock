import glob
import os
import json


def get_configs(config_key):
    """
    Getting App Config from ``constants.py``

    :param config_key: Key of desired config
    :return: value of desired config
    """
    with open('configs.json', 'r') as json_file:
        configs = json.load(json_file)
    return configs[config_key]


def delete_user_image_file(_path):
    os.remove(_path)


def get_list_of_files():
    return glob.glob(os.path.join(get_configs('images_path'), '*.*'))


def get_all_user_ids_from_files():
    """
    Generate ID for new user.
    :return:
    """
    files = get_list_of_files()
    return list(set(map(lambda x: x.split(get_configs('images_path'))[1].split('_')[0], files)))


def generate_next_user_id_from_files():
    """
    Generate ID for new user.
    :return:
    """
    files = get_list_of_files()
    if not files:
        return '0000'
    return '{:04d}'.format(
        max(list(set(map(lambda x: int(x.split(get_configs('images_path'))[1].split('_')[0]), files)))) + 1)
