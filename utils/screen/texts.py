import cv2

from constants import get_configs


def add_title_to_screen(_frame, _text, _color=(200, 200, 200)):
    """
    Show title on a frame

    :param _frame: Input frame
    :param _text: Input text
    :param _color: Input color
    """
    cv2.putText(_frame, _text, (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 6)
    cv2.putText(_frame, _text, (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, _color, 2)


def add_subtitle_to_screen(_frame, _text, _color=(200, 200, 200)):
    """
    Show subtitle on a frame

    :param _frame: Input frame
    :param _text: Input text
    :param _color: Input color
    """
    cv2.putText(_frame, _text, (30, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 4)
    cv2.putText(_frame, _text, (30, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, _color, 1)


def add_description_to_screen(_frame, _text, _color=(200, 200, 200)):
    """
    Show description on a frame

    :param _frame: Input frame
    :param _text: Input text
    :param _color: Input color
    """
    cv2.putText(_frame, _text, (30, 90), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 4)
    cv2.putText(_frame, _text, (30, 90), cv2.FONT_HERSHEY_DUPLEX, 0.7, _color, 1)


def show_loading_on_screen():
    """
    Show loading on a frame
    """
    cap = cv2.VideoCapture(get_configs('camera_arg'))
    ret_add, _frame = cap.read()
    add_title_to_screen(_frame, 'LOADING...', (0, 200, 200))
    cv2.imshow('Frame', _frame)
    _key = cv2.waitKey(1)
