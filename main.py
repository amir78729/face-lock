import cv2
from face_recognition_module import FaceRecognition
from constants import *
from utils.screen.faces import draw_rectangle_on_screen, show_faces_on_screen
from utils.user.add import add_user_image_to_dataset
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

        # Detect Faces
        try:
            face_locations, face_names = fr.recognize_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                color = (0, 0, 200) if name == 'Unknown' else (0, 200, 0)
                _id = name.split('_')[0]
                draw_rectangle_on_screen(
                    frame,
                    face_loc[0],
                    face_loc[1],
                    face_loc[2],
                    face_loc[3],
                    _color=(0, 0, 200) if name == 'Unknown'
                    else (0, 200, 200) if _id in get_configs('admin_users')
                    else (0, 200, 0),
                    _text='{}{}'.format('*' if _id in get_configs('admin_users') else '', _id)
                )
        except Exception as e:
            show_faces_on_screen(frame)

        cv2.imshow('Frame', frame)

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

        if key == ESCAPE:
            break

    cap.release()
    cv2.destroyAllWindows()
