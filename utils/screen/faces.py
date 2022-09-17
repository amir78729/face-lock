import cv2
from face_recognition_module import FaceRecognition
from utils.screen.texts import add_description_to_screen


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
