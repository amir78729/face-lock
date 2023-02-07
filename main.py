import cv2

from constants import *
from face_recognition_module import FaceRecognition
from utils.screen.faces import show_recognized_faces_on_screen
from utils.user.add import add_user
from utils.user.delete import delete_user

if __name__ == '__main__':
    # Encode faces.py from a folder
    fr = FaceRecognition()
    fr.load_encoding_images(get_configs('images_path'))

    # Load Camera
    cap = cv2.VideoCapture(get_configs('camera_arg'))
    # CAMERA_IP = 'http://192.168.1.110:8080/video'

    while True:
        ret, frame = cap.read()
        if not frame.any():
            raise Exception('CAMERA NOT FOUND')

        show_recognized_faces_on_screen(frame, fr)

        key = cv2.waitKey(1)
        if key == ord('a'):
            add_user(fr)

        if key == ord('d'):
            delete_user(fr)

        if key == ESCAPE or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
