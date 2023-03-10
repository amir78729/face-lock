import cv2
import time

from utils.screen.faces import show_detected_faces_on_screen
from utils.screen.texts import add_title_to_screen, add_subtitle_to_screen, add_description_to_screen
from utils.encryption import get_encrypted_password
from utils.files import get_configs
from utils.user.retrieve import get_username_by_id
from utils.log import log
from constants.keys import *
from constants.colors import *
from utils.screen.texts import add_time_to_screen
from utils.system import is_raspberry
from utils.screen.capture import get_raspberry_frames
from utils.keypad import read_keypad, KEYPAD_INPUTS


def is_user_admin(_fr):
    """
    Check if User is Admin
    :param _fr: face recognition module
    :return: is user admin
    """
    _id = ''
    is_authentication_strict = get_configs('authentication')['strict_authentication']

    if is_raspberry:
        frames, stream_capture = get_raspberry_frames()
        for f in frames:
            _frame = f.array
            detected_faces = []
            try:
                add_time_to_screen(_frame)
                face_locations, face_names = _fr.recognize_known_faces(_frame)

                for face_loc, name in zip(face_locations, face_names):
                    detected_faces.append(name.split('_')[0])
            except Exception as e:
                print(e)

            is_a_face_detected, face_locations = show_detected_faces_on_screen(_fr, _frame)

            add_title_to_screen(_frame, 'AUTHENTICATION', YELLOW)
            add_subtitle_to_screen(_frame, 'please enter your admin ID: ' + _id)

            if not is_a_face_detected:
                add_description_to_screen(_frame, 'NO FACE DETECTED!', RED)

            if is_authentication_strict:
                if is_a_face_detected and _id in detected_faces:
                    if _id in get_configs('authentication')['admin_users']:
                        add_description_to_screen(_frame, 'PRESS ENTER TO CONTINUE!', GREEN)
                    else:
                        add_description_to_screen(_frame, 'YOU ARE NOT AN ADMIN!', RED)
                elif _id != '':
                    add_description_to_screen(_frame, 'YOUR ID IS NOT "{}"'.format(_id), RED)

            cv2.imshow('Frame', _frame)
            _key = cv2.waitKey(1)
            key_keypad = read_keypad()
            stream_capture.truncate(0)

            if _key != -1:
                if _key == DELETE or key_keypad == KEYPAD_INPUTS['D']:
                    _id = _id[:-1]
                elif _key == ESCAPE or key_keypad == KEYPAD_INPUTS['#']:
                    break
                elif (_key == ENTER or key_keypad == KEYPAD_INPUTS['*']) and _id != '':
                    if get_configs('logging')['use_logging_in_admin_login']:
                        log('admin entered user id "{}"'.format(_id))
                    if not is_authentication_strict or _id in detected_faces:
                        return _id in get_configs('authentication')['admin_users']
                    if get_configs('logging')['use_logging_in_admin_login']:
                        log('face for id "{}" was not detected'.format(_id))
                else:
                    _id += chr(_key)
                    # TODO: add keypad input
                    _id = _id.replace('_', ' ')
    else:
        _cap = cv2.VideoCapture(get_configs('general')['camera_arg'])
        while True:
            ret_add, _frame = _cap.read()
            detected_faces = []
            try:
                add_time_to_screen(_frame)
                face_locations, face_names = _fr.recognize_known_faces(_frame)

                for face_loc, name in zip(face_locations, face_names):
                    detected_faces.append(name.split('_')[0])
            except Exception as e:
                print(e)

            is_a_face_detected, face_locations = show_detected_faces_on_screen(_fr, _frame)

            add_title_to_screen(_frame, 'AUTHENTICATION', YELLOW)
            add_subtitle_to_screen(_frame, 'please enter your admin ID: ' + _id)

            if not is_a_face_detected:
                add_description_to_screen(_frame, 'NO FACE DETECTED!', RED)

            if is_authentication_strict:
                if is_a_face_detected and _id in detected_faces:
                    if _id in get_configs('authentication')['admin_users']:
                        add_description_to_screen(_frame, 'PRESS ENTER TO CONTINUE!', GREEN)
                    else:
                        add_description_to_screen(_frame, 'YOU ARE NOT AN ADMIN!', RED)
                elif _id != '':
                    add_description_to_screen(_frame, 'YOUR ID IS NOT "{}"'.format(_id), RED)

            cv2.imshow('Frame', _frame)
            _key = cv2.waitKey(1)

            if _key != -1:
                if _key == DELETE:
                    _id = _id[:-1]
                elif _key == ESCAPE:
                    break
                elif _key == ENTER and _id != '':
                    if get_configs('logging')['use_logging_in_admin_login']:
                        log('admin entered user id "{}"'.format(_id))
                    if not is_authentication_strict or _id in detected_faces:
                        return _id in get_configs('authentication')['admin_users']
                    if get_configs('logging')['use_logging_in_admin_login']:
                        log('face for id "{}" was not detected'.format(_id))
                else:
                    _id += chr(_key)
                    _id = _id.replace('_', ' ')


def is_admin_user_authenticated(_fr, retry):
    """
    Check if admin entered the password correctly

    :param _fr: face recognition module
    :param retry: show error on page
    :return:
    """
    _password = ''

    if is_raspberry:
        frames, stream_capture = get_raspberry_frames()
        for f in frames:
            _frame = f.array
            add_time_to_screen(_frame)
            show_detected_faces_on_screen(_fr, _frame)

            add_title_to_screen(_frame, 'AUTHENTICATION', YELLOW)
            add_subtitle_to_screen(_frame, 'please enter the password: ' + len(_password) * '*')
            if retry:
                add_description_to_screen(_frame, 'WRONG PASSWORD! TRY AGAIN...', RED)

            cv2.imshow('Frame', _frame)
            _key = cv2.waitKey(1)
            key_keypad = read_keypad()
            stream_capture.truncate(0)

            if _key != -1:
                if _key == DELETE or key_keypad == KEYPAD_INPUTS['D']:
                    _password = _password[:-1]
                elif _key == ESCAPE or key_keypad == KEYPAD_INPUTS['#']:
                    break
                elif (_key == ENTER or key_keypad == KEYPAD_INPUTS['*']) and _password != '':
                    return get_encrypted_password(_password) == get_configs('authentication')[
                        'admin_encrypted_password']
                else:
                    # TODO
                    _password += chr(_key)
                    _password = _password.replace('_', ' ')
    else:
        _cap = cv2.VideoCapture(get_configs('general')['camera_arg'])
        while True:
            ret_add, _frame = _cap.read()
            add_time_to_screen(_frame)
            show_detected_faces_on_screen(_fr, _frame)

            add_title_to_screen(_frame, 'AUTHENTICATION', YELLOW)
            add_subtitle_to_screen(_frame, 'please enter the password: ' + len(_password) * '*')
            if retry:
                add_description_to_screen(_frame, 'WRONG PASSWORD! TRY AGAIN...', RED)

            cv2.imshow('Frame', _frame)
            _key = cv2.waitKey(1)

            if _key != -1:
                if _key == DELETE:
                    _password = _password[:-1]
                elif _key == ESCAPE:
                    break
                elif _key == ENTER and _password != '':
                    return get_encrypted_password(_password) == get_configs('authentication')['admin_encrypted_password']
                else:
                    _password += chr(_key)
                    _password = _password.replace('_', ' ')


def enter_user(_fr):
    def get_name(_id):
        try:
            return get_username_by_id(_id)
        except KeyError:
            return _id
    if is_raspberry:
        frames, stream_capture = get_raspberry_frames()
        _frame = None
        for f in frames:
            _frame = f.array
            break
        add_time_to_screen(_frame)
        face_locations, face_names = _fr.recognize_known_faces(_frame)

        try:
            if len(face_locations) > 1:
                add_title_to_screen(_frame, 'DOOR CANNOT BE OPENED!', RED)
                add_subtitle_to_screen(_frame, 'More than one faces were detected')
                log('unsuccessful entrance, more than one faces detected')
            else:
                name = get_name(face_names[0])
                if name == 'Unknown' or len(face_locations) != 1:
                    add_title_to_screen(_frame, 'DOOR CANNOT BE OPENED!', RED)
                    add_subtitle_to_screen(_frame, 'You are not able to enter')
                    add_description_to_screen(_frame, "please call system's administrator", YELLOW)
                    log('unsuccessful entrance, unauthorized access')
                else:
                    add_title_to_screen(_frame, 'DOOR IS OPEN', GREEN)
                    add_subtitle_to_screen(_frame, 'WELCOME!')
                    add_description_to_screen(_frame, "Don't forget to close the door!", YELLOW)
                    log('"{}" entered'.format(name.split('_')[0]))
        except (IndexError, TypeError):
            add_title_to_screen(_frame, 'DOOR CANNOT BE OPENED!', RED)
            add_subtitle_to_screen(_frame, 'No face was detected!', YELLOW)
            add_description_to_screen(_frame, "Please try again...")
            log('unsuccessful entrance, no face detected')

        cv2.imshow('Frame', _frame)
        _key = cv2.waitKey(1)
        stream_capture.truncate(0)
        time.sleep(3)
    else:
        cap = cv2.VideoCapture(get_configs('general')['camera_arg'])
        ret_add, _frame = cap.read()
        add_time_to_screen(_frame)
        face_locations, face_names = _fr.recognize_known_faces(_frame)

        try:
            if len(face_locations) > 1:
                add_title_to_screen(_frame, 'DOOR CANNOT BE OPENED!', RED)
                add_subtitle_to_screen(_frame, 'More than one faces were detected')
                log('unsuccessful entrance, more than one faces detected')
            else:
                name = get_name(face_names[0])
                if name == 'Unknown' or len(face_locations) != 1:
                    add_title_to_screen(_frame, 'DOOR CANNOT BE OPENED!', RED)
                    add_subtitle_to_screen(_frame, 'You are not able to enter')
                    add_description_to_screen(_frame, "please call system's administrator", YELLOW)
                    log('unsuccessful entrance, unauthorized access')
                else:
                    add_title_to_screen(_frame, 'DOOR IS OPEN', GREEN)
                    add_subtitle_to_screen(_frame, 'WELCOME!')
                    add_description_to_screen(_frame, "Don't forget to close the door!", YELLOW)
                    log('"{}" entered'.format(name.split('_')[0]))
        except (IndexError, TypeError):
            add_title_to_screen(_frame, 'DOOR CANNOT BE OPENED!', RED)
            add_subtitle_to_screen(_frame, 'No face was detected!', YELLOW)
            add_description_to_screen(_frame, "Please try again...")
            log('unsuccessful entrance, no face detected')

        cv2.imshow('Frame', _frame)
        _key = cv2.waitKey(1)
        time.sleep(3)

