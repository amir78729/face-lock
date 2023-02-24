import cv2

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
        camera = PiCamera()
        camera.resolution = RESOLUTION
        camera.framerate = FRAME_RATE
        raw_capture = PiRGBArray(camera, size=RESOLUTION)
        return camera.capture(raw_capture, format="bgr", use_video_port=True)
    ret, frame = cap.read()
    if not frame.any():
        raise Exception('CAMERA NOT FOUND')
    return frame


def terminate_capture():
    cap.release()
    cv2.destroyAllWindows()
