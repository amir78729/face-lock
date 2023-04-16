import cv2

from constants.keys import *
from constants.colors import *
from utils.files import get_configs
from time import ctime
from utils.system import is_raspberry
from utils.screen.capture import get_raspberry_frames
from utils.led import led_on, led_off


def add_title_to_screen(_frame, _text, _color=WHITE):
    """
    Show title on a frame

    :param _frame: Input frame
    :param _text: Input text
    :param _color: Input color
    """
    cv2.putText(_frame, _text, (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, BLACK, 6)
    cv2.putText(_frame, _text, (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, _color, 2)


def add_subtitle_to_screen(_frame, _text, _color=WHITE):
    """
    Show subtitle on a frame

    :param _frame: Input frame
    :param _text: Input text
    :param _color: Input color
    """
    cv2.putText(_frame, _text, (30, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, BLACK, 4)
    cv2.putText(_frame, _text, (30, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, _color, 1)


def add_description_to_screen(_frame, _text, _color=WHITE):
    """
    Show description on a frame

    :param _frame: Input frame
    :param _text: Input text
    :param _color: Input color
    """
    cv2.putText(_frame, _text, (30, 90), cv2.FONT_HERSHEY_DUPLEX, 0.7, BLACK, 4)
    cv2.putText(_frame, _text, (30, 90), cv2.FONT_HERSHEY_DUPLEX, 0.7, _color, 1)


def add_time_to_screen(_frame, _color=WHITE):
    """
    Show Time

    :param _frame: Input frame
    :param _color: Input color
    """
    time = ctime()
    textsize = cv2.getTextSize(time, cv2.FONT_HERSHEY_DUPLEX, 0.7, 2)[0]
    textX = (_frame.shape[1] - textsize[0] - 30)
    textY = (_frame.shape[0] - textsize[1] - 30)
    # textY = 30
    cv2.putText(_frame, time, (textX, textY), cv2.FONT_HERSHEY_DUPLEX, 0.7, BLACK, 4)
    cv2.putText(_frame, time, (textX, textY), cv2.FONT_HERSHEY_DUPLEX, 0.7, _color, 1)


def add_debug_text_to_screen(_frame, text, line_num=0,  _color=CYAN):
    """
    Show Time

    :param _frame: Input frame
    :param _color: Input color
    """
    textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.7, 2)[0]
    textX = (30)
    textY = (_frame.shape[0] - textsize[1] - 30 - (line_num * 30))

    cv2.putText(_frame, text, (textX, textY), cv2.FONT_HERSHEY_DUPLEX, 0.7, BLACK, 4)
    cv2.putText(_frame, text, (textX, textY), cv2.FONT_HERSHEY_DUPLEX, 0.7, _color, 1)


def show_loading_on_screen():
    """
    Show loading on a frame
    """
    if is_raspberry:
        frames, stream_capture = get_raspberry_frames()
        _frame = None
        for f in frames:
            _frame = f.array
            break
        add_time_to_screen(_frame)
        add_title_to_screen(_frame, 'LOADING...', YELLOW)
        cv2.imshow('FACE LOCK', _frame)
        _key = cv2.waitKey(1)
        stream_capture.truncate(0)
    else:
        cap = cv2.VideoCapture(get_configs('general')['camera_arg'])
        ret_add, _frame = cap.read()
        add_time_to_screen(_frame)
        add_title_to_screen(_frame, 'LOADING...', YELLOW)
        cv2.imshow('FACE LOCK', _frame)
        _key = cv2.waitKey(1)

