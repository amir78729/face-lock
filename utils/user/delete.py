import glob
import os
import cv2

from constants import *
from utils.screen.texts import add_title_to_screen, add_subtitle_to_screen, show_loading_on_screen


def get_all_user_ids():
    """
    Generate ID for new user.
    :return:
    """
    files = glob.glob(os.path.join(get_configs('images_path'), '*.*'))  # TODO: make function
    return list(set(map(lambda x: x.split(get_configs('images_path'))[1].split('_')[0], files)))


def enter_id():
    """
    Removing files for input id

    :return: a list of files for deleting
    """
    _cap = cv2.VideoCapture(0)
    _id = ''
    admins = get_configs('admin_users')

    while True:
        ret_add, _frame = _cap.read()

        add_title_to_screen(_frame, 'DELETE USER', (0, 0, 200))
        add_subtitle_to_screen(_frame, 'please enter id to delete: ' + _id)

        cv2.imshow('Frame', _frame)
        _key = cv2.waitKey(1)

        if _key != -1:
            if _key == DELETE:
                _id = _id[:-1]
            elif _key == ESCAPE:
                break
            elif _key == ENTER:
                if _id in get_all_user_ids() and _id not in admins:
                    files = glob.glob(os.path.join(get_configs('images_path'), '*.*'))  # TODO: make function
                    return [x for x in files if _id in x]

            else:
                _id += chr(_key)
                _id = _id.replace('_', ' ')


def remove_user():
    file_paths = enter_id()
    [os.remove(path) for path in file_paths]
    show_loading_on_screen()
