import copy
import glob
import os
import cv2

from constants import *
from utils.screen.faces import show_detected_faces_on_screen
from utils.screen.texts import add_title_to_screen, add_subtitle_to_screen, show_loading_on_screen, \
    add_description_to_screen


def enter_user_name():
    """
    Enter Username
    :return:
    """
    _cap = cv2.VideoCapture(0)
    _name = ''
    while True:
        ret_add, frame_add = _cap.read()
        is_a_face_detected = show_detected_faces_on_screen(frame_add)

        add_title_to_screen(frame_add, 'ADD IMAGE: ENTER NAME')
        add_subtitle_to_screen(frame_add, 'please enter your name: ' + _name)
        if not is_a_face_detected:
            add_description_to_screen(frame_add, 'NO FACE DETECTED!', (0, 0, 200))

        cv2.imshow('Frame', frame_add)
        _key = cv2.waitKey(1)

        if _key != -1:
            if _key == DELETE:
                _name = _name[:-1]
            elif _key == ESCAPE:
                break
            elif _key == ENTER and _name != '':
                return _name
            else:
                _name += chr(_key)
                _name = _name.replace('_', ' ')


def generate_user_id():
    """
    Generate ID for new user.
    :return:
    """
    files = glob.glob(os.path.join(get_configs('images_path'), '*.*'))
    if not files:
        return '0000'
    return '{:04d}'.format(
        max(list(set(map(lambda x: int(x.split(get_configs('images_path'))[1].split('_')[0]), files)))) + 1)


def take_and_save_user_image(_name, _index):
    """
    Take a Picture from user and save taken image as a file
    :param _name: User ID
    :param _index:  Replica Index
    :return:
    """
    cap = cv2.VideoCapture(get_configs('camera_arg'))
    while True:
        ret_add, frame_add = cap.read()
        frame_add_copy = copy.deepcopy(frame_add)
        is_a_face_detected = show_detected_faces_on_screen(frame_add)

        add_title_to_screen(frame_add,
                            'ADD IMAGE: ADD IMAGE TO DATABASE ({} / {})'.format(_index, get_configs('images_per_user')))
        add_subtitle_to_screen(frame_add, 'press ENTER to take picture')
        if not is_a_face_detected:
            add_description_to_screen(frame_add, 'NO FACE DETECTED!', (0, 0, 200))

        cv2.imshow('Frame', frame_add)
        _key = cv2.waitKey(1)

        if _key == ENTER and is_a_face_detected:
            cv2.imwrite('images/{}_{}.jpg'.format(_name, _index), frame_add_copy)
            break

        if _key == ESCAPE:
            break


def add_user_image_to_dataset():
    """
    Take Picture from user ``images_per_user`` times

    :return:
    """
    name = generate_user_id()
    [take_and_save_user_image(_name=name, _index=i + 1) for i in range(get_configs('images_per_user'))]
    show_loading_on_screen()
