import cv2
import os
import argparse

from constants import *
from utils.face_recognition import FaceRecognition
from utils.screen.faces import show_recognized_faces_on_screen
from utils.user.add import add_user
from utils.user.delete import delete_user
from utils.user.authentication import enter_user
from utils.files import get_configs
from utils.keypad import read_keypad, KEYPAD_INPUTS
from utils.screen.texts import add_time_to_screen, add_debug_text_to_screen
from utils.screen.capture import get_raspberry_frames
from utils.system import is_raspberry
from colorama import Style, Fore
from time import time


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", dest="debug", help="Debug Mode", type=bool)
    args = parser.parse_args()
    is_debug_mode = args.debug

    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(args.debug)
        print((Fore.CYAN if is_debug_mode else Fore.GREEN) + CE_LOGO + Style.RESET_ALL)
        print((Fore.CYAN if is_debug_mode else Fore.GREEN) + FACE_LOCK_SINGLE_LINE + Style.RESET_ALL)
        if is_debug_mode:
            print(Fore.CYAN +
                  '░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░')
            print('░░░░░░░░░░░░░░░░░░░░░ DEBUG MODE IS ACTIVATED! ░░░░░░░░░░░░░░░░░░░░░')
            print('░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░' + Style.RESET_ALL)
        fr = FaceRecognition()
        fr.load_encoding_images(get_configs('general')['images_path'])

        if is_raspberry:
            frames, stream_capture = get_raspberry_frames()
            for f in frames:
                frame = f.array
                add_time_to_screen(frame)
                show_recognized_faces_on_screen(frame, fr)
                key = cv2.waitKey(1)
                key_keypad = read_keypad()
                stream_capture.truncate(0)
                if key == ENTER or key_keypad == KEYPAD_INPUTS['*']:
                    enter_user(fr)
                if key == ord('a') or key == ord('A') or key_keypad == KEYPAD_INPUTS['A']:
                    add_user(fr)
                elif key == ord('d') or key == ord('D') or key_keypad == KEYPAD_INPUTS['D']:
                    delete_user(fr)
                elif key == ESCAPE or key == ord('q') or key == ord('Q') or key_keypad == KEYPAD_INPUTS['#']:
                    break
        else:
            frame_start = time()
            previous_frame_duration = 0
            is_frame_duration_increased = False
            while True:
                cap = cv2.VideoCapture(get_configs('general')['camera_arg'])
                ret, frame = cap.read()
                add_time_to_screen(frame)
                if is_debug_mode:
                    add_debug_text_to_screen(frame, 'TOLERANCE: {}'.format(get_configs('face_recognition')['tolerance']))
                    add_debug_text_to_screen(frame, 'NUM_JITTERS: {}'.format(get_configs('face_recognition')['num_jitters']), 1)
                    add_debug_text_to_screen(frame, 'NUMBER_OF_TIMES_TO_UPSAMPLE: {}'.format(get_configs('face_recognition')['number_of_times_to_upsample']), 2)
                    add_debug_text_to_screen(frame, 'MODEL: {}'.format(get_configs('face_recognition')['model']), 3)
                    add_debug_text_to_screen(frame, 'FRAME DURATION: {}'.format(previous_frame_duration), 4, _color=(GREEN if is_frame_duration_increased else RED))
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
                frame_end = time()
                if is_debug_mode:
                    current_frame_duration = frame_end - frame_start
                    is_frame_duration_increased = current_frame_duration < previous_frame_duration
                    previous_frame_duration = current_frame_duration
                    print(Fore.CYAN + '> FRAME DURATION:   ' + str(previous_frame_duration) + Style.RESET_ALL)
                    frame_start = frame_end
            cap.release()
            cv2.destroyAllWindows()
    except KeyboardInterrupt:
        print(Fore.RED + '\nExiting the Program...' + Style.RESET_ALL)
