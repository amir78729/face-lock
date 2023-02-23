import cv2

from constants.keys import *
from utils.face_recognition import FaceRecognition
from utils.screen.faces import show_recognized_faces_on_screen
from utils.user.add import add_user
from utils.user.delete import delete_user
from utils.user.authentication import enter_user
from utils.files import get_configs
from utils.screen.texts import add_time_to_screen
import os

is_raspberry = os.uname()[4][:3] == 'arm'

if is_raspberry:
    from picamera.array import PiRGBArray
    from picamera import PiCamera

if __name__ == '__main__':
    fr = FaceRecognition()
    fr.load_encoding_images(get_configs('general')['images_path'])

    def run(_frame, _raw_capture):
        add_time_to_screen(_frame)
        show_recognized_faces_on_screen(_frame, fr)
        key = cv2.waitKey(1)
        # For Raspberry Pi Boards
        if _raw_capture:
            _raw_capture.truncate(0)
        if key == ENTER:
            enter_user(fr)
        if key == ord('a'):
            add_user(fr)
        elif key == ord('d'):
            delete_user(fr)
        elif key == ESCAPE or key == ord('q'):
            return False
        return True


    if is_raspberry:
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        raw_capture = PiRGBArray(camera, size=(640, 480))

        for f in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
            frame = f.array
            should_continue = run(frame, raw_capture)
            if not should_continue:
                break
    else:
        # Load Camera
        cap = cv2.VideoCapture(get_configs('general')['camera_arg'])
        # CAMERA_IP = 'http://192.168.1.110:8080/video'
        while True:
            ret, frame = cap.read()
            if not frame.any():
                raise Exception('CAMERA NOT FOUND')

            should_continue = run(frame, None)
            if not should_continue:
                break

        cap.release()
        cv2.destroyAllWindows()
