import cv2

from constants.keys import *
from constants.colors import *
from utils.files import get_configs
from time import ctime


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


def show_loading_on_screen():
    """
    Show loading on a frame
    """
    cap = cv2.VideoCapture(get_configs('general')['camera_arg'])
    ret_add, _frame = cap.read()
    add_time_to_screen(_frame)
    add_title_to_screen(_frame, 'LOADING...', YELLOW)
    cv2.imshow('Frame', _frame)
    _key = cv2.waitKey(1)
