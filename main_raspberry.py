import cv2

from constants.keys import *
from utils.face_recognition import FaceRecognition
from utils.screen.faces import show_recognized_faces_on_screen
from utils.user.add import add_user
from utils.user.delete import delete_user
from utils.user.authentication import enter_user
from utils.files import get_configs
from picamera.array import PiRGBArray
from picamera import PiCamera

if __name__ == '__main__':
    fr = FaceRecognition()
    fr.load_encoding_images(get_configs('general')['images_path'])
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        show_recognized_faces_on_screen(image, fr)
        key = cv2.waitKey(1)
        rawCapture.truncate(0)
        if key == ENTER:
            enter_user(fr)
        if key == ord('a'):
            add_user(fr)
        elif key == ord('d'):
            delete_user(fr)
        elif key == ESCAPE or key == ord('q'):
            break
