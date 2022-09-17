import cv2
from constants import *
from utils.screen.texts import add_title_to_screen, add_subtitle_to_screen
from utils.screen.faces import show_faces_on_screen
from utils.security import get_encrypted_password


def is_user_admin():
    _cap = cv2.VideoCapture(0)
    _id = ''
    while True:
        ret_add, frame_add = _cap.read()
        show_faces_on_screen(frame_add)

        add_title_to_screen(frame_add, 'ADD USER: LOGIN')
        add_subtitle_to_screen(frame_add, 'please enter your admin ID: ' + _id)
        cv2.imshow('Frame', frame_add)
        key_add = cv2.waitKey(1)

        if key_add != -1:
            if key_add == DELETE:
                _id = _id[:-1]
            elif key_add == ESCAPE:
                break
            elif key_add == ENTER and _id != '':
                return _id in get_configs('admin_users')
            else:
                _id += chr(key_add)
                _id = _id.replace('_', ' ')


def is_admin_user_authenticated():
    _cap = cv2.VideoCapture(0)
    _password = ''
    while True:
        ret_add, frame_add = _cap.read()
        show_faces_on_screen(frame_add)

        add_title_to_screen(frame_add, 'ADD USER: LOGIN')
        add_subtitle_to_screen(frame_add, 'please enter the password: ' + len(_password) * '*')
        cv2.imshow('Frame', frame_add)
        key_add = cv2.waitKey(1)

        if key_add != -1:
            if key_add == DELETE:
                _password = _password[:-1]
            elif key_add == ESCAPE:
                break
            elif key_add == ENTER and _password != '':
                return get_encrypted_password(_password) == get_configs('admin_password')
            else:
                _password += chr(key_add)
                _password = _password.replace('_', ' ')
