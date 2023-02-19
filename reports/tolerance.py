import matplotlib.pyplot as plt
import numpy as np
import math


def face_distance_to_conf(_face_distance, face_match_threshold=0.6):
    if _face_distance > face_match_threshold:
        _range = (1.0 - face_match_threshold)
        linear_val = (1.0 - _face_distance) / (_range * 2.0)
        return linear_val
    else:
        _range = face_match_threshold
        linear_val = 1.0 - (_face_distance / (_range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))


if __name__ == '__main__':
    face_distance = np.arange(0, 1, 0.01)
    tolerance_range = np.arange(0.1, 1, 0.1)
    colors = ['#ff6961', '#ffb54c', '#f8d66d', '#7abd7e', '#8cd47e', '#7abd7e', '#f8d66d', '#ffb54c', '#ff6961']
    plt.rcParams['figure.figsize'] = (12, 12)
    for tolerance, color in zip(tolerance_range, colors):
        confidence_score = [face_distance_to_conf(_face_distance, tolerance) for _face_distance in face_distance]
        plt.subplot(3, 3, int(tolerance * 10))
        plt.tight_layout(pad=5.0)
        plt.plot(face_distance, confidence_score, color=color)
        plt.ylim(0, 1)
        plt.axvline(x=tolerance, color=color, alpha=0.3, linestyle='--')
        plt.xlabel('Face Distance')
        plt.ylabel('Confidence Score')
        plt.title('tolerance = {}'.format(round(tolerance, 1)))
    plt.savefig('charts/tolerance-report.png')

