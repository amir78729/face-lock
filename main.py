import cv2
from face_recognition_module import FaceRecognition
from constants import *
from utils.screen.faces import draw_rectangle_on_screen, show_detected_faces_on_screen, show_recognized_faces_on_screen
from utils.user.add import add_user_image_to_dataset
from utils.user.delete import remove_user
from utils.user.authentication import is_user_admin, is_admin_user_authenticated

if __name__ == '__main__':
    # Encode faces.py from a folder
    fr = FaceRecognition()
    fr.load_encoding_images(get_configs('images_path'))

    # Load Camera
    cap = cv2.VideoCapture(get_configs('camera_arg'))
    # CAMERA_IP = 'http://192.168.1.110:8080/video'

    while True:
        ret, frame = cap.read()
        if not frame.any():
            raise Exception('CAMERA NOT FOUND')

        show_recognized_faces_on_screen(frame, fr)

        key = cv2.waitKey(1)
        if key == ord('a'):
            if is_user_admin(fr):
                _try = 0
                while _try < get_configs('wrong_password_limit'):
                    if is_admin_user_authenticated(retry=_try != 0):
                        add_user_image_to_dataset()
                        fr.load_encoding_images(get_configs('images_path'))
                        break
                    else:
                        _try += 1
            else:
                print('YOU ARE NOT AN ADMIN')

        if key == ord('d'):
            if is_user_admin(fr):
                _try = 0
                while _try < get_configs('wrong_password_limit'):
                    if is_admin_user_authenticated(retry=_try != 0):
                        remove_user()
                        fr.load_encoding_images(get_configs('images_path'))
                        break
                    else:
                        _try += 1
            else:
                print('YOU ARE NOT AN ADMIN')

        if key == ESCAPE:
            break

    cap.release()
    cv2.destroyAllWindows()
