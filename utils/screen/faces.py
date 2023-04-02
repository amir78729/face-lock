import cv2

from constants import *
from utils.face_recognition import FaceRecognition
from utils.user.retrieve import get_username_by_id
from utils.files import get_configs


def draw_rectangle_on_screen(_frame, _y1, _x2, _y2, _x1, _color=GREEN, _text=''):
    """
    Draw a rectangle on a frame

    :param _frame: Input frame
    :param _y1: Y1
    :param _x2: X2
    :param _y2: Y2
    :param _x1: X1
    :param _color: Color
    :param _text: Title
    :return:
    """
    if _text == '':
        cv2.rectangle(_frame, (_x1, _y1), (_x2, _y2), BLACK, 6)
    else:
        cv2.rectangle(_frame, (_x1, _y1 - 40), (_x2, _y2), BLACK, 6)
        cv2.rectangle(_frame, (_x1, _y1 - 40), (_x2, _y1), BLACK, 6)

    cv2.rectangle(_frame, (_x1, _y1), (_x2, _y2), _color, 2)
    if _text != '':
        cv2.rectangle(_frame, (_x1, _y1 - 40), (_x2, _y1), BLACK, -1)
        cv2.rectangle(_frame, (_x1, _y1 - 40), (_x2, _y1), _color, 2)
        cv2.putText(_frame, _text, (_x1 + 10, _y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, BLACK, 6)
        cv2.putText(_frame, _text, (_x1 + 10, _y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, _color, 2)


def show_detected_faces_on_screen(_fr, _frame):
    """
    Show detected faces on a frame

    :param _fr: face recognition module
    :param _frame: Input frame
    :return: boolean value for checking if any face was detected in input frame
    """
    try:
        _fr = FaceRecognition()
        _face_locations = _fr.detect_faces(_frame)
        if _face_locations.any():
            for _face_loc in _face_locations:
                draw_rectangle_on_screen(
                    _frame,
                    _face_loc[0],
                    _face_loc[1],
                    _face_loc[2],
                    _face_loc[3],
                    _color=WHITE,
                )
        return _face_locations.any(), _face_locations
    except Exception as e:
        print(e)


def show_recognized_faces_on_screen(_frame, _fr):
    """
    Show recognized faces on a frame

    :param _frame: Input frame
    :param _fr: face recognition module
    :return:
    """
    def get_name(_id):
        try:
            return get_username_by_id(_id)
        except KeyError:
            return _id
    try:
        face_locations, face_names = _fr.recognize_known_faces(_frame)

        for face_loc, name in zip(face_locations, face_names):
            _id = name.split('_')[0]
            draw_rectangle_on_screen(
                _frame,
                face_loc[0],
                face_loc[1],
                face_loc[2],
                face_loc[3],
                _color=RED if name == 'Unknown'
                else YELLOW if _id in get_configs('authentication')['admin_users']
                else GREEN,
                _text='{}{}'.format('*' if _id in get_configs('authentication')['admin_users'] else '', get_name(_id))
            )
    except Exception as e:
        show_detected_faces_on_screen(_fr, _frame)

    cv2.imshow('FACE LOCK', _frame)
