import cv2

from constants import *
from utils.screen.faces import show_detected_faces_on_screen
from utils.screen.texts import add_title_to_screen, add_subtitle_to_screen, add_description_to_screen
from utils.security import get_encrypted_password


def is_user_admin(_fr):
    """
    Check if User is Admin
    :param _fr: face recognition module
    :return: is user admin
    """
    _cap = cv2.VideoCapture(0)
    _id = ''
    is_authentication_strict = get_configs('strict_authentication')

    while True:
        ret_add, _frame = _cap.read()
        detected_faces = []
        try:
            face_locations, face_names = _fr.recognize_known_faces(_frame)
            for face_loc, name in zip(face_locations, face_names):
                detected_faces.append(name.split('_')[0])
        except Exception:
            pass

        is_a_face_detected = show_detected_faces_on_screen(_frame)

        add_title_to_screen(_frame, 'AUTHENTICATION')
        add_subtitle_to_screen(_frame, 'please enter your admin ID: ' + _id)

        if not is_a_face_detected:
            add_description_to_screen(_frame, 'NO FACE DETECTED!', (0, 0, 200))

        if is_authentication_strict:
            if is_a_face_detected and _id in detected_faces:
                if _id in get_configs('admin_users'):
                    add_description_to_screen(_frame, 'PRESS ENTER TO CONTINUE!', (0, 200, 0))
                else:
                    add_description_to_screen(_frame, 'YOU ARE NOT AN ADMIN!', (0, 0, 200))
            elif _id != '':
                add_description_to_screen(_frame, 'YOUR ID IS NOT "{}"'.format(_id), (0, 0, 200))

        cv2.imshow('Frame', _frame)
        _key = cv2.waitKey(1)

        if _key != -1:
            if _key == DELETE:
                _id = _id[:-1]
            elif _key == ESCAPE:
                break
            elif _key == ENTER and _id != '':
                if not is_authentication_strict or _id in detected_faces:
                    return _id in get_configs('admin_users')
            else:
                _id += chr(_key)
                _id = _id.replace('_', ' ')


def is_admin_user_authenticated(retry):
    """
    Check if admin entered the password correctly

    :param retry: show error on page
    :return:
    """
    _cap = cv2.VideoCapture(0)
    _password = ''
    while True:
        ret_add, _frame = _cap.read()
        show_detected_faces_on_screen(_frame)

        add_title_to_screen(_frame, 'AUTHENTICATION')
        add_subtitle_to_screen(_frame, 'please enter the password: ' + len(_password) * '*')
        if retry:
            add_description_to_screen(_frame, 'WRONG PASSWORD! TRY AGAIN...', (0, 0, 200))
        cv2.imshow('Frame', _frame)
        _key = cv2.waitKey(1)

        if _key != -1:
            if _key == DELETE:
                _password = _password[:-1]
            elif _key == ESCAPE:
                break
            elif _key == ENTER and _password != '':
                return get_encrypted_password(_password) == get_configs('admin_password')
            else:
                _password += chr(_key)
                _password = _password.replace('_', ' ')
