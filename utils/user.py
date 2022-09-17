import glob
import os
import copy
from constants import *
from utils.screen import *


def enter_user_name():
    _cap = cv2.VideoCapture(0)
    _name = ''
    while True:
        ret_add, frame_add = _cap.read()
        show_faces_on_screen(frame_add)

        add_title_to_screen(frame_add, 'ADD IMAGE: ENTER NAME')
        add_subtitle_to_screen(frame_add, 'please enter your name: ' + _name)
        cv2.imshow('Frame', frame_add)
        key_add = cv2.waitKey(1)

        if key_add != -1:
            if key_add == DELETE:
                _name = _name[:-1]
            elif key_add == ESCAPE:
                break
            elif key_add == ENTER and _name != '':
                return _name
            else:
                _name += chr(key_add)
                _name = _name.replace('_', ' ')


def generate_user_id():
    files = glob.glob(os.path.join(get_configs('images_path'), '*.*'))
    if not files:
        return '0000'
    return '{:04d}'.format(
        max(list(set(map(lambda x: int(x.split(get_configs('images_path'))[1].split('_')[0]), files)))) + 1)


def take_and_save_user_image(_name, _index):
    cap = cv2.VideoCapture(get_configs('camera_arg'))
    while True:
        ret_add, frame_add = cap.read()
        frame_add_copy = copy.deepcopy(frame_add)
        show_faces_on_screen(frame_add)
        add_title_to_screen(
            frame_add,
            'ADD IMAGE: ADD IMAGE TO DATABASE ({} / {})'.format(_index, get_configs('images_per_user'))
        )
        add_subtitle_to_screen(frame_add, 'press ENTER to take picture')
        cv2.imshow('Frame', frame_add)
        key_add = cv2.waitKey(1)

        if key_add == ENTER:
            cv2.imwrite('images/{}_{}.jpg'.format(_name, _index), frame_add_copy)
            break


def add_user_image_to_dataset():
    name = generate_user_id()
    [take_and_save_user_image(_name=name, _index=i+1) for i in range(get_configs('images_per_user'))]
    show_loading_on_screen()