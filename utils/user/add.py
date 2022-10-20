import copy

import cv2

from constants import *
from utils.files import generate_next_user_id_from_files
from utils.keypad import convert_keypad_input_sequence_to_string, standardize_keypad_input_sequence, \
    KEYPAD_VALID_NUMERIC_INPUTS
from utils.screen.faces import show_detected_faces_on_screen
from utils.screen.texts import add_title_to_screen, add_subtitle_to_screen, show_loading_on_screen, \
    add_description_to_screen
from utils.user.authentication import is_user_admin, is_admin_user_authenticated
from utils.logger import log


def enter_user_name(_fr):
    """
    Enter Username
    :return:
    """
    _cap = cv2.VideoCapture(0)
    _name = ''

    def get_name():
        if get_configs('using_numeric_keypad'):
            return convert_keypad_input_sequence_to_string(standardize_keypad_input_sequence(_name))
        return _name

    while True:
        ret_add, _frame = _cap.read()
        is_a_face_detected = show_detected_faces_on_screen(_fr, _frame)

        add_title_to_screen(_frame, 'ADD IMAGE: ENTER NAME')
        add_subtitle_to_screen(_frame, 'please enter your name: ' + get_name())
        if not is_a_face_detected:
            add_description_to_screen(_frame, 'NO FACE DETECTED!', (0, 0, 200))

        cv2.imshow('Frame', _frame)
        _key = cv2.waitKey(1)

        if _key != -1:
            if _key == DELETE:
                _name = _name[:-1]
            elif _key == ESCAPE:
                break
            elif _key == ENTER and _name != '':
                if get_configs('logging')['use_logging_in_admin_login']:
                    log('username entered: "{}"'.format(get_name()))
                return get_name()
            else:
                if get_configs('using_numeric_keypad'):
                    if chr(_key) in KEYPAD_VALID_NUMERIC_INPUTS:
                        _name += chr(_key)
                else:
                    _name += chr(_key)
                    _name = _name.replace('_', ' ')


def take_and_save_user_image(_name, _index, _fr):
    """
    Take a Picture from user and save taken image as a file
    :param _fr: User ID
    :param _name: User ID
    :param _index:  Replica Index
    :return:
    """
    cap = cv2.VideoCapture(get_configs('camera_arg'))
    while True:
        ret_add, _frame = cap.read()
        _frame_copy = copy.deepcopy(_frame)
        is_a_face_detected = show_detected_faces_on_screen(_fr, _frame)

        add_title_to_screen(_frame,
                            'ADD IMAGE: ADD IMAGE TO DATABASE ({} / {})'.format(_index, get_configs('images_per_user')))
        add_subtitle_to_screen(_frame, 'press ENTER to take picture')
        if not is_a_face_detected:
            add_description_to_screen(_frame, 'NO FACE DETECTED!', (0, 0, 200))

        cv2.imshow('Frame', _frame)
        _key = cv2.waitKey(1)

        if _key == ENTER and is_a_face_detected:
            cv2.imwrite('{}/{}_{}.jpg'.format(get_configs('images_path'), _name, _index), _frame_copy)
            break

        if _key == ESCAPE:
            break


def add_username_by_user_id(_id, _username):
    """
    Getting username by id

    :param _id: user id
    :param _username: username
    :return:
    """
    with open(get_configs('names_data'), 'r') as names_data:
        json_decoded = json.load(names_data)
    json_decoded[_id] = _username
    with open(get_configs('names_data'), 'w') as names_data:
        json.dump(json_decoded, names_data)

        if get_configs('logging')['use_logging_in_add_user']:
            log('name "{}" added for user "{}"'.format(_username, _id))


def add_user_image_to_dataset(_fr):
    """
    Take Picture from user ``images_per_user`` times

    :return:
    """
    new_id = generate_next_user_id_from_files()
    if get_configs('store_usernames'):
        new_username = enter_user_name(_fr)
        if new_username and new_username != '':
            add_username_by_user_id(new_id, new_username)
    [take_and_save_user_image(_name=new_id, _index=i + 1, _fr=_fr) for i in range(get_configs('images_per_user'))]
    if get_configs('logging')['use_logging_in_add_user']:
        log('user "{}" added successfully'.format(new_id))
    show_loading_on_screen()


def add_user(_fr):
    if get_configs('logging')['use_logging_in_add_user']:
        log('adding user...')
    if is_user_admin(_fr):
        if get_configs('logging')['use_logging_in_admin_login']:
            log('admin entered user id')
        _try = 0
        while _try < get_configs('wrong_password_limit'):
            if is_admin_user_authenticated(_fr, retry=_try != 0):
                if get_configs('logging')['use_logging_in_admin_login']:
                    log('admin logged in')
                add_user_image_to_dataset(_fr)
                _fr.load_encoding_images(get_configs('images_path'))
                break
            else:
                if get_configs('logging')['use_logging_in_wrong_password']:
                    log('wrong password')
                _try += 1

    else:
        if get_configs('logging')['use_logging_in_add_user']:
            log('adding canceled')
