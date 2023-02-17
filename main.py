import cv2

from constants.keys import *
from utils.face_recognition import FaceRecognition
from utils.screen.faces import show_recognized_faces_on_screen
from utils.user.add import add_user
from utils.user.delete import delete_user
from utils.user.authentication import enter_user
from utils.files import get_configs

if __name__ == '__main__':
    # Encode faces.py from a folder
    fr = FaceRecognition()
    fr.load_encoding_images(get_configs('general')['images_path'])

    # Load Camera
    cap = cv2.VideoCapture(get_configs('general')['camera_arg'])
    # CAMERA_IP = 'http://192.168.1.110:8080/video'

    while True:
        ret, frame = cap.read()
        if not frame.any():
            raise Exception('CAMERA NOT FOUND')

        show_recognized_faces_on_screen(frame, fr)

        key = cv2.waitKey(1)
        if key == ENTER:
            enter_user(fr)
        if key == ord('a'):
            add_user(fr)
        elif key == ord('d'):
            delete_user(fr)
        elif key == ESCAPE or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
