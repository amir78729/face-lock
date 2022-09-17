import glob
import os

import cv2
from constants import *
from utils.screen.texts import add_title_to_screen, add_subtitle_to_screen, add_description_to_screen
from utils.screen.faces import show_detected_faces_on_screen
from utils.security import get_encrypted_password


def is_user_admin(_fr):
    _cap = cv2.VideoCapture(0)
    _id = ''

    while True:
        ret_add, frame_add = _cap.read()
        detected_faces = []
        try:
            face_locations, face_names = _fr.recognize_known_faces(frame_add)
            for face_loc, name in zip(face_locations, face_names):
                detected_faces.append(name.split('_')[0])
        except Exception:
            pass

        is_a_face_detected = show_detected_faces_on_screen(frame_add)

        add_title_to_screen(frame_add, 'ADD USER: LOGIN')
        add_subtitle_to_screen(frame_add, 'please enter your admin ID: ' + _id)

        if not is_a_face_detected:
            add_description_to_screen(frame_add, 'NO FACE DETECTED!', (0, 0, 200))
        elif _id in detected_faces:
            if _id in get_configs('admin_users'):
                add_description_to_screen(frame_add, 'PRESS ENTER TO CONTINUE!', (0, 200, 0))
            else:
                add_description_to_screen(frame_add, 'YOU ARE NOT AN ADMIN!', (0, 0, 200))
        elif _id != '':
            add_description_to_screen(frame_add, 'YOUR ID IS NOT "{}"'.format(_id), (0, 0, 200))

        cv2.imshow('Frame', frame_add)
        _key = cv2.waitKey(1)

        if _key != -1:
            if _key == DELETE:
                _id = _id[:-1]
            elif _key == ESCAPE:
                break
            elif _key == ENTER and _id != '' and _id in detected_faces:  # admin should be in front of the camera
                return _id in get_configs('admin_users')
            else:
                _id += chr(_key)
                _id = _id.replace('_', ' ')


def is_admin_user_authenticated(retry):
    _cap = cv2.VideoCapture(0)
    _password = ''
    while True:
        ret_add, frame_add = _cap.read()
        show_detected_faces_on_screen(frame_add)

        add_title_to_screen(frame_add, 'ADD USER: LOGIN')
        add_subtitle_to_screen(frame_add, 'please enter the password: ' + len(_password) * '*')
        if retry:
            add_description_to_screen(frame_add, 'WRONG PASSWORD! TRY AGAIN...', (0, 0, 200))
        cv2.imshow('Frame', frame_add)
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
