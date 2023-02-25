import cv2

from constants.keys import *
from utils.face_recognition import FaceRecognition
from utils.screen.faces import show_recognized_faces_on_screen
from utils.user.add import add_user
from utils.user.delete import delete_user
from utils.user.authentication import enter_user
from utils.files import get_configs
from utils.screen.texts import add_time_to_screen
from utils.screen.capture import capture_frame, terminate_capture


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.load_encoding_images(get_configs('general')['images_path'])

    while True:
        frame = capture_frame()
        add_time_to_screen(frame)
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
    terminate_capture()

