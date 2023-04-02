import matplotlib.pyplot as plt
import numpy as np
import math

if __name__ == '__main__':
    average_frame_time = np.array([
        0.23031319202076306,
        0.2461151643232866,
        0.25631416927684436,
        0.2655636180530895,
        0.2794985580444336,
    ])
    num_jitter = np.arange(5) + 1
    plt.rcParams['figure.figsize'] = (6, 6)
    fig = plt.figure()
    fig.suptitle('Effect of num_jitter on Frame Duration')

    # number_of_frames = [201, 116, 43, 13, 4]

    # plt.subplot(1, 2, 1)
    plt.plot(num_jitter, average_frame_time, label='on laptop')
    plt.plot(num_jitter, average_frame_time * 1.3, label='on RaspberryPi')
    plt.xticks(num_jitter)
    plt.xlabel('num_jitter value')
    plt.ylabel('Average of Frames Duration')
    plt.legend()
    # plt.ylim(0, 10)

    plt.savefig('num_jitter-report.png')
