# import face_recognition
from services.face_recognition import face_encodings, face_locations, face_distance, compare_faces
import cv2
import os
import glob
import numpy as np
from tqdm import tqdm
from utils.files import get_configs


class FaceRecognition:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path

        :param images_path: Directory of Images
        :return:
        """
        # Load Images
        images_path = glob.glob(os.path.join(images_path, '*.*'))

        print('{} encoding images found.'.format(len(images_path)))

        try:
            # Store image encoding and names
            for img_path in tqdm(images_path):
                img = cv2.imread(img_path)
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Get the filename only from the initial file path.
                basename = os.path.basename(img_path)
                (filename, ext) = os.path.splitext(basename)
                # Get encoding
                img_encoding = face_encodings(rgb_img)[0]

                # Store file name and file encoding
                self.known_face_encodings.append(img_encoding)
                self.known_face_names.append(filename)
            print('Encoding images loaded')
        except Exception as e:
            print(e)

    def recognize_known_faces(self, frame):
        """
        Face Recognition Process for a frame

        :param frame: Input Image
        :return:
        """
        small_frame = cv2.resize(
            frame,
            (0, 0),
            fx=self.frame_resizing,
            fy=self.frame_resizing
        )
        # Find all the faces.py and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        _face_locations = face_locations(small_frame, get_configs('face_recognition')['number_of_times_to_upsample'], get_configs('face_recognition')['model'])
        _face_encodings = face_encodings(small_frame, _face_locations)

        face_names = []
        for face_encoding in _face_encodings:
            # See if the face is a match for the known face(s)
            matches = compare_faces(
                self.known_face_encodings,
                face_encoding,
                tolerance=get_configs('face_recognition')['tolerance']
            )
            name = 'Unknown'
            face_distances = face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        _face_locations = np.array(_face_locations)
        _face_locations = _face_locations / self.frame_resizing
        return _face_locations.astype(int), face_names

    def detect_faces(self, frame):
        """
        Face Detection Process for a frame

        :param frame: Input Image
        :return:
        """
        small_frame = cv2.resize(
            frame,
            (0, 0),
            fx=self.frame_resizing,
            fy=self.frame_resizing
        )
        small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        _face_locations = face_locations(small_frame, get_configs('face_recognition')['number_of_times_to_upsample'], get_configs('face_recognition')['model'])
        _face_locations = np.array(_face_locations)
        _face_locations = _face_locations / self.frame_resizing
        return _face_locations.astype(int)
