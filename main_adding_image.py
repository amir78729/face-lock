import glob
import os

import cv2
import copy
from simple_facerec import FaceRecognition

ESCAPE = 27
ENTER = 13
TAB = 9
DELETE = 127
CAMERA_IP = 0
# CAMERA_IP = 'http://192.168.1.110:8080/video'

def add_title_to_page(_frame, _text, _color=(200, 200, 200)):
    cv2.putText(_frame, _text, (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 6)
    cv2.putText(_frame, _text, (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, _color, 2)


def add_subtitle_to_page(_frame, _text, _color=(200, 200, 200)):
    cv2.putText(_frame, _text, (30, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 4)
    cv2.putText(_frame, _text, (30, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, _color, 1)


def add_description_to_page(_frame, _text, _color=(200, 200, 200)):
    cv2.putText(_frame, _text, (30, 90), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 4)
    cv2.putText(_frame, _text, (30, 90), cv2.FONT_HERSHEY_DUPLEX, 0.7, _color, 1)


def draw_rectangle(_frame, _y1, _x2, _y2, _x1, _color=(0, 200, 0), _text=''):
    cv2.putText(_frame, _text, (_x1, _y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 6)
    cv2.putText(_frame, _text, (_x1, _y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, _color, 2)
    cv2.rectangle(_frame, (_x1, _y1), (_x2, _y2), (0, 0, 0), 6)
    cv2.rectangle(_frame, (_x1, _y1), (_x2, _y2), _color, 2)


def show_faces(_frame):
    try:
        _sfr = FaceRecognition()
        _face_locations = _sfr.detect_faces(_frame)
        if _face_locations.any():
            for _face_loc in _face_locations:
                draw_rectangle(
                    _frame,
                    _face_loc[0],
                    _face_loc[1],
                    _face_loc[2],
                    _face_loc[3],
                    _color=(200, 200, 200),
                )
        else:
            add_description_to_page(_frame, 'NO FACE DETECTED!', (0, 0, 200))

    except Exception as e:
        print(e)


# def enter_name():
#     _cap = cv2.VideoCapture(0)
#     _name = ''
#     while True:
#         ret_add, frame_add = _cap.read()
#         show_faces(frame_add)
# 
#         add_title_to_page(frame_add, 'ADD IMAGE: ENTER NAME')
#         add_subtitle_to_page(frame_add, 'please enter your name: ' + _name)
#         cv2.imshow("Frame", frame_add)
#         key_add = cv2.waitKey(1)
# 
#         if key_add != -1:
#             if key_add == DELETE:
#                 _name = _name[:-1]
#             elif key_add == ESCAPE:
#                 break
#             elif key_add == ENTER and _name != '':
#                 return _name
#             else:
#                 _name += chr(key_add)
#                 _name = _name.replace('_', ' ')


def generate_name():
    files = glob.glob(os.path.join('images/', "*.*"))
    if not files:
        return '0000'
    return "{:04d}".format(max(list(set(map(lambda x: int(x.split('images/')[1].split('_')[0]), files)))) + 1)


def take_and_save_picture(_name, _index):
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(CAMERA_IP)
    while True:
        ret_add, frame_add = cap.read()
        frame_add_copy = copy.deepcopy(frame_add)
        show_faces(frame_add)
        add_title_to_page(frame_add, 'ADD IMAGE: ADD IMAGE TO DATABASE ({} / 3)'.format(_index))
        add_subtitle_to_page(frame_add, 'press ENTER to take picture')
        cv2.imshow("Frame", frame_add)
        key_add = cv2.waitKey(1)

        if key_add == ENTER:
            cv2.imwrite('images/{}_{}.jpg'.format(_name, _index), frame_add_copy)
            break


def show_loading():
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(CAMERA_IP)
    
    ret_add, frame_loading = cap.read()
    add_title_to_page(frame_loading, 'LOADING...', (0, 200, 200))
    cv2.imshow("Frame", frame_loading)

def add_pic_to_dataset():
    name = generate_name()
    [take_and_save_picture(_name=name, _index=i+1) for i in range(3)]
    show_loading()


if __name__ == '__main__':
    # Encode faces from a folder
    sfr = FaceRecognition()
    sfr.load_encoding_images("images/")

    # Load Camera
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(CAMERA_IP)

    while True:
        ret, frame = cap.read()
        if not frame.any():
            raise Exception('CAMERA NOT FOUND')

        # Detect Faces
        try:
            face_locations, face_names = sfr.recognize_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                color = (0, 0, 200) if name == 'Unknown' else (0, 200, 0)
                draw_rectangle(
                    frame,
                    face_loc[0],
                    face_loc[1],
                    face_loc[2],
                    face_loc[3],
                    _color=(0, 0, 200) if name == 'Unknown' else (0, 200, 0),
                    _text=name.split('_')[0]
                )
        except ValueError:
            pass

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == ord('a'):
            add_pic_to_dataset()
            sfr.load_encoding_images("images/")

        if key == ESCAPE:
            break

    cap.release()
    cv2.destroyAllWindows()