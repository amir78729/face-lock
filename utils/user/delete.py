import cv2
import json

from constants.colors import *
from constants.keys import *
from utils.files import get_list_of_files, get_all_user_ids_from_files, delete_user_image_file
from utils.screen.texts import add_title_to_screen, add_subtitle_to_screen, show_loading_on_screen
from utils.user.authentication import is_user_admin, is_admin_user_authenticated
from utils.log import log
from utils.files import get_configs


def enter_id():
    """
    Removing files for input id

    :return: a list of files for deleting
    """
    _cap = cv2.VideoCapture(0)
    _id = ''
    admins = get_configs('authentication')['admin_users']

    while True:
        ret_add, _frame = _cap.read()

        add_title_to_screen(_frame, 'DELETE USER', RED)
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
                    return [x for x in files if _id in x], _id

            else:
                _id += chr(_key)
                _id = _id.replace('_', ' ')


def delete_username_by_user_id(_id):
    """
    Delete username by id

    :param _id: user id
    :return:
    """
    with open(get_configs('general')['names_data'], 'r') as names_data:
        json_decoded = json.load(names_data)
    json_decoded.pop(_id, None)

    with open(get_configs('general')['names_data'], 'w') as names_data:
        json.dump(json_decoded, names_data)


def delete_user_images():
    file_paths, _id = enter_id()
    delete_username_by_user_id(_id)
    [delete_user_image_file(path) for path in file_paths]
    if get_configs('logging')['use_logging_in_delete_user']:
        log('user "{}" deleted successfully'.format(_id))
    show_loading_on_screen()


def delete_user(_fr):
    if get_configs('logging')['use_logging_in_delete_user']:
        log('deleting user...')
    if is_user_admin(_fr):
        _try = 0
        while _try < get_configs('authentication')['wrong_password_limit']:
            if is_admin_user_authenticated(_fr, retry=_try != 0):
                if get_configs('logging')['use_logging_in_admin_login']:
                    log('admin logged in')
                delete_user_images()
                _fr.load_encoding_images(
                    get_configs('general')['images_path'])  # FIXME after deleting user still is detected on screen
                break
            else:
                if get_configs('logging')['use_logging_in_wrong_password']:
                    log('wrong password')
                _try += 1
    else:
        if get_configs('logging')['use_logging_in_delete_user']:
            log('deleting canceled')
