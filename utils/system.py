import os

is_raspberry = os.uname()[4][:3] == 'arm'

if is_raspberry:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
