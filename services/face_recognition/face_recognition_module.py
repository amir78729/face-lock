import PIL.Image
import dlib
import numpy as np
from PIL import ImageFile
import face_recognition_models
import os

if os.uname()[4][:3] == 'CPU':
    try:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        from mtcnn.mtcnn import MTCNN

        mtcnn_face_detector = MTCNN()
    except:
        pass

ImageFile.LOAD_TRUNCATED_IMAGES = True

face_detector = dlib.get_frontal_face_detector()

predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)

cnn_face_detection_model = face_recognition_models.cnn_face_detector_model_location()
cnn_face_detector = dlib.cnn_face_detection_model_v1(cnn_face_detection_model)

face_recognition_model = face_recognition_models.face_recognition_model_location()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)


def _rect_to_css(rect):
    """
    Convert a dlib 'rect' object to a plain tuple in (top, right, bottom, left) order

    :param rect: a dlib 'rect' object
    :return: a plain tuple representation of the rect in (top, right, bottom, left) order
    """
    return rect.top(), rect.right(), rect.bottom(), rect.left()


def _css_to_rect(css):
    """
    Convert a tuple in (top, right, bottom, left) order to a dlib `rect` object

    :param css:  plain tuple representation of the rect in (top, right, bottom, left) order
    :return: a dlib `rect` object
    """
    return dlib.rectangle(css[3], css[0], css[1], css[2])


def _trim_css_to_bounds(css, image_shape):
    """
    Make sure a tuple in (top, right, bottom, left) order is within the bounds of the image.

    :param css:  plain tuple representation of the rect in (top, right, bottom, left) order
    :param image_shape: numpy shape of the image array
    :return: a trimmed plain tuple representation of the rect in (top, right, bottom, left) order
    """
    return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)


def face_distance(_face_encodings, face_to_compare):
    """
    Given a list of face encodings, compare them to a known face encoding and get a euclidean distance
    for each comparison face. The distance tells you how similar the faces are.

    :param _face_encodings: List of face encodings to compare
    :param face_to_compare: A face encoding to compare against
    :return: A numpy ndarray with the distance for each face in the same order as the 'faces' array
    """
    if len(_face_encodings) == 0:
        return np.empty(0)

    return np.linalg.norm(_face_encodings - face_to_compare, axis=1)


def _raw_face_locations(img, number_of_times_to_upsample=1, model='hog'):
    """
    Returns an array of bounding boxes of human faces in an image

    :param img: An image (as a numpy array)
    :param number_of_times_to_upsample: How many times to upsample the image looking for faces. Higher numbers find
    smaller faces.
    :param model: Which face detection model to use. 'hog' is less accurate but faster on CPUs. 'cnn' is a more accurate
                  deep-learning model which is GPU/CUDA accelerated (if available). The default is 'hog'.
    :return: A list of dlib 'rect' objects of found face locations
    """
    if model == 'cnn':
        return cnn_face_detector(img, number_of_times_to_upsample)
    else:
        return face_detector(img, number_of_times_to_upsample)


def face_locations(img, number_of_times_to_upsample=1, model='hog'):
    """
    Returns an array of bounding boxes of human faces in an image

    :param img: An image (as a numpy array)
    :param number_of_times_to_upsample: How many times to upsample the image looking for faces. Higher numbers find
    smaller faces.
    :param model: Which face detection model to use. 'hog' is less accurate but faster on CPUs. 'cnn' is a more accurate
                  deep-learning model which is GPU/CUDA accelerated (if available). The default is 'hog'.
    :return: A list of tuples of found face locations in css (top, right, bottom, left) order
    """
    if model == 'cnn':
        return [
                _trim_css_to_bounds(
                    _rect_to_css(face.rect), img.shape
                    ) for face in _raw_face_locations(
                        img, number_of_times_to_upsample, 'cnn'
                    )
        ]
    else:
        return [
            _trim_css_to_bounds(
                _rect_to_css(face), img.shape
            ) for face in _raw_face_locations(
                img, number_of_times_to_upsample, model
            )
        ]


def _raw_face_locations_batched(images, number_of_times_to_upsample=1, batch_size=128):
    """
    Returns a 2d array of dlib rects of human faces in an image using the cnn face detector

    :param images: A list of images (each as a numpy array)
    :param number_of_times_to_upsample: How many times to upsample the image looking for faces. Higher numbers find
    smaller faces.
    :return: A list of dlib 'rect' objects of found face locations
    """
    return cnn_face_detector(images, number_of_times_to_upsample, batch_size=batch_size)


def batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128):
    """
    Returns a 2d array of bounding boxes of human faces in an image using the cnn face detector
    If you are using a GPU, this can give you much faster results since the GPU
    can process batches of images at once. If you aren't using a GPU, you don't need this function.

    :param images: A list of images (each as a numpy array)
    :param number_of_times_to_upsample: How many times to upsample the image looking for faces. Higher numbers find
    smaller faces.
    :param batch_size: How many images to include in each GPU processing batch.
    :return: A list of tuples of found face locations in css (top, right, bottom, left) order
    """
    def convert_cnn_detections_to_css(detections):
        return [_trim_css_to_bounds(_rect_to_css(face.rect), images[0].shape) for face in detections]

    raw_detections_batched = _raw_face_locations_batched(images, number_of_times_to_upsample, batch_size)

    return list(map(convert_cnn_detections_to_css, raw_detections_batched))


def _raw_face_landmarks(face_image, _face_locations=None):
    if _face_locations is None:
        _face_locations = _raw_face_locations(face_image)
    else:
        _face_locations = [_css_to_rect(face_location) for face_location in _face_locations]

    pose_predictor = pose_predictor_68_point
    return [pose_predictor(face_image, face_location) for face_location in _face_locations]


def face_landmarks(face_image, _face_locations=None):
    """
    Given an image, returns a dict of face feature locations (eyes, nose, etc.) for each face in the image

    :param face_image: image to search
    :param _face_locations: Optionally provide a list of face locations to check.
    :return: A list of dicts of face feature locations (eyes, nose, etc)
    """
    landmarks = _raw_face_landmarks(face_image, _face_locations)
    landmarks_as_tuples = [[(p.x, p.y) for p in landmark.parts()] for landmark in landmarks]
    return [{
        'nose_tip': [points[4]],
        'left_eye': points[2:4],
        'right_eye': points[0:2],
    } for points in landmarks_as_tuples]


def face_encodings(face_image, known_face_locations=None, num_jitters=1):
    """
    Given an image, return the 128-dimension face encoding for each face in the image.

    :param face_image: The image that contains one or more faces
    :param known_face_locations: Optional - the bounding boxes of each face if you already know them.
    :param num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but
    slower (i.e. 100 is 100x slower)
    :return: A list of 128-dimensional face encodings (one for each face in the image)
    """
    raw_landmarks = _raw_face_landmarks(face_image, known_face_locations)
    return [
        np.array(
            face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)
        ) for raw_landmark_set in raw_landmarks
    ]


def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    """
    Compare a list of face encodings against a candidate encoding to see if they match.

    :param known_face_encodings: A list of known face encodings
    :param face_encoding_to_check: A single face encoding to compare against the list
    :param tolerance: How much distance between faces to consider it a match. Lower is stricter. 0.6 is typical best
    performance.
    :return: A list of True/False values indicating which known_face_encodings match the face encoding to check
    """
    return list(face_distance(known_face_encodings, face_encoding_to_check) <= tolerance)
