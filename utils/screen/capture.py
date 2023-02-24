import cv2
import numpy as np
import time

from utils.system import is_raspberry
from utils.files import get_configs

if is_raspberry:
    from picamera.array import PiRGBArray
    from picamera import PiCamera

RESOLUTION = (640, 480)
FRAME_RATE = 32


def get_raspberry_frames():
    camera = PiCamera()
    camera.resolution = RESOLUTION
    camera.framerate = FRAME_RATE
    raw_capture = PiRGBArray(camera, size=RESOLUTION)
    return [camera.capture_continuous(raw_capture, format="bgr", use_video_port=True), raw_capture]


cap = cv2.VideoCapture(get_configs('general')['camera_arg'])  # TODO GLOBALIZE


def capture_frame():
    if is_raspberry:
        with PiCamera() as camera:
            camera.resolution = (100, 100)
            camera.framerate = 24
            # time.sleep(2)
            output = np.empty((112 * 128 * 3,), dtype=np.uint8)
            camera.capture(output, 'rgb')
            output = output.reshape((112, 128, 3))
            output = output[:100, :100, :]
            # print(output)
            return output
        # camera = PiCamera()
        # camera.resolution = RESOLUTION
        # camera.framerate = FRAME_RATE
        # time.sleep(2)
        # frame = np.empty((240 * 320 * 3,), dtype=np.uint8)
        # camera.capture(frame, 'bgr')
        # frame = frame.reshape((240, 320, 3))
        # return frame
    ret, frame = cap.read()
    if not frame.any():
        raise Exception('CAMERA NOT FOUND')
    return frame


def terminate_capture():
    cap.release()
    cv2.destroyAllWindows()
