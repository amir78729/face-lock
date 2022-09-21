import cv2

from constants import *
from utils.files import get_list_of_files, get_all_user_ids_from_files, delete_user_image_file
from utils.screen.texts import add_title_to_screen, add_subtitle_to_screen, show_loading_on_screen
from utils.user.authentication import is_user_admin, is_admin_user_authenticated


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
                if _id in get_all_user_ids_from_files() and _id not in admins:
                    files = get_list_of_files()
                    return [x for x in files if _id in x]

            else:
                _id += chr(_key)
                _id = _id.replace('_', ' ')


def delete_user_images():
    file_paths = enter_id()
    [delete_user_image_file(path) for path in file_paths]
    show_loading_on_screen()


def delete_user(_fr):
    if is_user_admin(_fr):
        _try = 0
        while _try < get_configs('wrong_password_limit'):
            if is_admin_user_authenticated(_fr, retry=_try != 0):
                delete_user_images()
                _fr.load_encoding_images(
                    get_configs('images_path'))  # FIXME after deleting user still is detected on screen
                break
            else:
                _try += 1
    else:
        print('YOU ARE NOT AN ADMIN')
