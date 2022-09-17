import cv2
from constants import get_configs
from face_recognition_module import FaceRecognition


def add_title_to_screen(_frame, _text, _color=(200, 200, 200)):
    cv2.putText(_frame, _text, (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 6)
    cv2.putText(_frame, _text, (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, _color, 2)


def add_subtitle_to_screen(_frame, _text, _color=(200, 200, 200)):
    cv2.putText(_frame, _text, (30, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 4)
    cv2.putText(_frame, _text, (30, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, _color, 1)


def add_description_to_screen(_frame, _text, _color=(200, 200, 200)):
    cv2.putText(_frame, _text, (30, 90), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 4)
    cv2.putText(_frame, _text, (30, 90), cv2.FONT_HERSHEY_DUPLEX, 0.7, _color, 1)


def draw_rectangle_on_screen(_frame, _y1, _x2, _y2, _x1, _color=(0, 200, 0), _text=''):
    cv2.putText(_frame, _text, (_x1, _y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 6)
    cv2.putText(_frame, _text, (_x1, _y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, _color, 2)
    cv2.rectangle(_frame, (_x1, _y1), (_x2, _y2), (0, 0, 0), 6)
    cv2.rectangle(_frame, (_x1, _y1), (_x2, _y2), _color, 2)


def show_faces_on_screen(_frame):
    try:
        _sfr = FaceRecognition()
        _face_locations = _sfr.detect_faces(_frame)
        if _face_locations.any():
            for _face_loc in _face_locations:
                draw_rectangle_on_screen(
                    _frame,
                    _face_loc[0],
                    _face_loc[1],
                    _face_loc[2],
                    _face_loc[3],
                    _color=(200, 200, 200),
                )
        else:
            add_description_to_screen(_frame, 'NO FACE DETECTED!', (0, 0, 200))
    except Exception as e:
        print(e)


def show_loading_on_screen():
    cap = cv2.VideoCapture(get_configs('camera_arg'))
    ret_add, frame_loading = cap.read()
    add_title_to_screen(frame_loading, 'LOADING...', (0, 200, 200))
    cv2.imshow('Frame', frame_loading)
