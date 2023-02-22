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
    # Encode faces.py from a folder
    fr = FaceRecognition()
    fr.load_encoding_images(get_configs('general')['images_path'])

    # Load Camera
    # cap = cv2.VideoCapture(get_configs('general')['camera_arg'])
    # CAMERA_IP = 'http://192.168.1.110:8080/video'
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # # grab the raw NumPy array representing the image, then initialize the timestamp
        # # and occupied/unoccupied text
        # image = frame.array
        # # show the frame
        # cv2.imshow("Frame", image)
        # key = cv2.waitKey(1) & 0xFF
        # # clear the stream in preparation for the next frame
        # rawCapture.truncate(0)
        # # if the `q` key was pressed, break from the loop
        # if key == ord("q"):
        #     break
        #
        # ####
        show_recognized_faces_on_screen(frame, fr)
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

    # while True:
    #     ret, frame = cap.read()
    #     if not frame.any():
    #         raise Exception('CAMERA NOT FOUND')
    #
    #     show_recognized_faces_on_screen(frame, fr)
    #
    #     key = cv2.waitKey(1)
    #     if key == ENTER:
    #         enter_user(fr)
    #     if key == ord('a'):
    #         add_user(fr)
    #     elif key == ord('d'):
    #         delete_user(fr)
    #     elif key == ESCAPE or key == ord('q'):
    #         break
    #
    # cap.release()
    # cv2.destroyAllWindows()


# # import the necessary packages
# from picamera.array import PiRGBArray
# from picamera import PiCamera
# import time
# import cv2
#
# # initialize the camera and grab a reference to the raw camera capture
# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.framerate = 32
# rawCapture = PiRGBArray(camera, size=(640, 480))
# # allow the camera to warmup
# time.sleep(0.1)
# # capture frames from the camera
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#     # grab the raw NumPy array representing the image, then initialize the timestamp
#     # and occupied/unoccupied text
#     image = frame.array
#     # show the frame
#     cv2.imshow("Frame", image)
#     key = cv2.waitKey(1) & 0xFF
#     # clear the stream in preparation for the next frame
#     rawCapture.truncate(0)
#     # if the `q` key was pressed, break from the loop
#     if key == ord("q"):
#         break
