import collections
import random

import cv2
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
from utils.led import led_on, led_off
from colorama import Style, Fore
from time import time


if __name__ == '__main__':
    # led_on()
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", dest="debug", help="Debug Mode", type=bool)
    args = parser.parse_args()
    is_debug_mode = args.debug

    # debugging variables
    fig = None
    if is_debug_mode:
        frame_start = time()
        previous_frame_duration = 0
        is_frame_duration_increased = False
        frame_durations = collections.deque([], 20)
        frame_number = 0
        num_all_faces = 0
        num_known_faces = 0
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(2, 2))
        ax = fig.add_subplot(1, 1, 1)
        xs = []
        ys = []
        def animate(i, _xs, _ys):
            global frame_number, previous_frame_duration
            _xs.append(frame_number)
            _ys.append(previous_frame_duration)
            _xs = _xs[-100:]
            _ys = _ys[-100:]
            ax.clear()
            if previous_frame_duration < 0.3:
                ax.plot(_xs, _ys, c='g')
            else:
                ax.plot(_xs, _ys, c='r')
            plt.xticks(fontsize=5)
            plt.yticks(fontsize=5)
            plt.grid(color='#333', linestyle='--', linewidth=0.5)
        ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100)

        def update_debug_params():
            global frame_start, previous_frame_duration, frame_number, is_frame_duration_increased
            frame_end = time()
            current_frame_duration = frame_end - frame_start
            is_frame_duration_increased = current_frame_duration < previous_frame_duration
            frame_durations.append(current_frame_duration)
            previous_frame_duration = current_frame_duration
            print(Fore.CYAN + '> FRAME DURATION: ' + str(previous_frame_duration) + Style.RESET_ALL)
            frame_start = frame_end
            frame_number += 1
            print('-' * 68)


        def show_debug_params(_frame):
            global frame_start, previous_frame_duration, frame_number, is_frame_duration_increased
            add_debug_text_to_screen(_frame, 'TOLERANCE: {}'.format(get_configs('face_recognition')['tolerance']))
            add_debug_text_to_screen(_frame, 'NUM_JITTERS: {}'.format(get_configs('face_recognition')['num_jitters']), 1)
            add_debug_text_to_screen(_frame, 'NUMBER_OF_TIMES_TO_UPSAMPLE: {}'.format(
                get_configs('face_recognition')['number_of_times_to_upsample']), 2)
            add_debug_text_to_screen(_frame, 'MODEL: {}'.format(get_configs('face_recognition')['model']), 3)
            add_debug_text_to_screen(_frame, 'CURRENT FRAME DURATION: {}'.format(format(previous_frame_duration, '.4f')), 4,
                                     _color=(GREEN if is_frame_duration_increased else RED))
            add_debug_text_to_screen(_frame, 'AVERAGE FRAME DURATION: {}'.format(
                format(np.mean(frame_durations), '.4f') if len(frame_durations) else '?'), 5, _color=YELLOW)
            add_debug_text_to_screen(_frame, 'CURRENT FRAME NUMBER: {}'.format(frame_number), 6)
            add_debug_text_to_screen(_frame, 'FACES(KNOWN): {}({})'.format(num_all_faces, num_known_faces), 7,
                                     _color=(GREEN if num_known_faces else RED))
            add_debug_text_to_screen(_frame, 'TRAINING DURATION: {}s'.format(format(training_duration, '.4f')), 8)
            add_debug_text_to_screen(_frame, 'IS_RASPBERRY: {}'.format(is_raspberry), 9)

    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print((Fore.CYAN if is_debug_mode else Fore.GREEN) + CE_LOGO + Style.RESET_ALL)
        print((Fore.CYAN if is_debug_mode else Fore.GREEN) + FACE_LOCK_SINGLE_LINE + Style.RESET_ALL)
        if is_debug_mode:
            print(Fore.CYAN +
                  '░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░')
            print('░░░░░░░░░░░░░░░░░░░░░ DEBUG MODE IS ACTIVATED! ░░░░░░░░░░░░░░░░░░░░░')
            print('░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░' + Style.RESET_ALL)
        fr = FaceRecognition()
        led_on()
        training_duration = fr.load_encoding_images(get_configs('general')['images_path'])
        led_off()

        if is_raspberry:
            frames, stream_capture = get_raspberry_frames()
            for f in frames:
                frame = f.array
                add_time_to_screen(frame)
                if is_debug_mode:
                    show_debug_params(frame)
                num_all_faces, num_known_faces = show_recognized_faces_on_screen(frame, fr, fig, is_debug_mode)
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
                    print(Fore.RED + '\nExiting the Program...' + Style.RESET_ALL)
                    break
                if is_debug_mode:
                    update_debug_params()
        else:
            while True:
                cap = cv2.VideoCapture(get_configs('general')['camera_arg'])
                ret, frame = cap.read()
                add_time_to_screen(frame)
                if is_debug_mode:
                    show_debug_params(frame)
                num_all_faces, num_known_faces = show_recognized_faces_on_screen(frame, fr, fig, is_debug_mode)
                key = cv2.waitKey(1)
                if key == ENTER:
                    enter_user(fr)
                if key == ord('a'):
                    add_user(fr)
                elif key == ord('d'):
                    delete_user(fr)
                elif key == ESCAPE or key == ord('q'):
                    print(Fore.RED + '\nExiting the Program...' + Style.RESET_ALL)
                    break
                if is_debug_mode:
                    update_debug_params()
            cap.release()
            cv2.destroyAllWindows()
    except KeyboardInterrupt:
        print(Fore.RED + '\nExiting the Program...' + Style.RESET_ALL)
