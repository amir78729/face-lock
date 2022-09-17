import cv2

from constants import get_configs
from face_recognition_module import FaceRecognition


def draw_rectangle_on_screen(_frame, _y1, _x2, _y2, _x1, _color=(0, 200, 0), _text=''):
    if _text == '':
        cv2.rectangle(_frame, (_x1, _y1), (_x2, _y2), (0, 0, 0), 6)
    else:
        cv2.rectangle(_frame, (_x1, _y1 - 40), (_x2, _y2), (0, 0, 0), 6)
        cv2.rectangle(_frame, (_x1, _y1 - 40), (_x2, _y1), (0, 0, 0), 6)

    cv2.rectangle(_frame, (_x1, _y1), (_x2, _y2), _color, 2)
    if _text != '':
        cv2.rectangle(_frame, (_x1, _y1 - 40), (_x2, _y1), (0, 0, 0), -1)
        cv2.rectangle(_frame, (_x1, _y1 - 40), (_x2, _y1), _color, 2)
        cv2.putText(_frame, _text, (_x1 + 10, _y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 6)
        cv2.putText(_frame, _text, (_x1 + 10, _y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, _color, 2)


def show_detected_faces_on_screen(_frame):
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
                    _color=(200, 200, 200),
                )
        return _face_locations.any()
    except Exception as e:
        print(e)


def show_recognized_faces_on_screen(_frame, _fr):
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
                _color=(0, 0, 200) if name == 'Unknown'
                else (0, 200, 200) if _id in get_configs('admin_users')
                else (0, 200, 0),
                _text='{}{}'.format('*' if _id in get_configs('admin_users') else '', _id)
            )
    except Exception as e:
        show_detected_faces_on_screen(_frame)
    cv2.imshow('Frame', _frame)
