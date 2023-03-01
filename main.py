import cv2

from constants import *
from utils.face_recognition import FaceRecognition
from utils.screen.faces import show_recognized_faces_on_screen
from utils.user.add import add_user
from utils.user.delete import delete_user
from utils.user.authentication import enter_user
from utils.files import get_configs
from utils.screen.texts import add_time_to_screen
from utils.screen.capture import capture_frame, terminate_capture, get_raspberry_frames
from utils.system import is_raspberry
from colorama import Style, Fore


if __name__ == '__main__':
    print(Fore.GREEN, FACE_LOCK, Style.RESET_ALL)
    fr = FaceRecognition()
    fr.load_encoding_images(get_configs('general')['images_path'])

    if is_raspberry:
        frames, stream_capture = get_raspberry_frames()
        for _frame in frames:
            frame = _frame.array
            add_time_to_screen(frame)
            show_recognized_faces_on_screen(frame, fr)
            key = cv2.waitKey(1)
            stream_capture.truncate(0)
            if key == ENTER:
                enter_user(fr)
            if key == ord('a'):
                add_user(fr)
            elif key == ord('d'):
                delete_user(fr)
            elif key == ESCAPE or key == ord('q'):
                break
    else:
        while True:
            cap = cv2.VideoCapture(get_configs('general')['camera_arg'])
            ret, frame = cap.read()
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
        cap.release()
        cv2.destroyAllWindows()

