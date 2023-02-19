import matplotlib.pyplot as plt
import numpy as np
import math

if __name__ == '__main__':
    average_frame_time = [
        104.234375,
        102.94358974358974,
        100.57788944723617,
        99.07562189054727,
        92.63425925925925,
    ]
    num_jitters = np.arange(5) + 1
    plt.rcParams['figure.figsize'] = (12, 6)
    fig = plt.figure()
    fig.suptitle('Effect of num_jitters on User Experience', fontsize=20)

    number_of_frames = [192, 195, 199, 205, 216]

    plt.subplot(1, 2, 1)
    plt.plot(num_jitters, average_frame_time)
    plt.xticks(num_jitters)
    plt.xlabel('num_jitters value')
    plt.ylabel('Average of Frames Duration in 20s')

    plt.subplot(1, 2, 2)
    plt.plot(num_jitters, number_of_frames)
    plt.xticks(num_jitters)
    plt.xlabel('num_jitters value')
    plt.ylabel('Number of Total Frames in 20s')

    plt.savefig('charts/number_jitters-report.png')
