import json
from utils.files import get_configs


def get_username_by_id(_id):
    """
    Getting username by id

    :param _id: user id
    :return: username
    """
    with open(get_configs('general')['names_data'], 'r') as json_file:
        names = json.load(json_file)
    return names[_id]
