import matplotlib.pyplot as plt
import numpy as np
import math

if __name__ == '__main__':
    average_frame_time = np.array([
        0.23655091632496228,
        0.29825854301452637,
        0.6062947403300892,
        1.8100770820270886,
        6.896197730844671,
    ])
    number_of_times_to_upsample = np.arange(5) + 1
    plt.rcParams['figure.figsize'] = (6, 6)
    # plt.rcParams['figure.figsize'] = (12, 6)
    fig = plt.figure()
    fig.suptitle('Effect of number_of_times_to_upsample on Frame Duration')

    # number_of_frames = [201, 116, 43, 13, 4]
    average_frame_time_jitter = np.array([
        0.23031319202076306,
        0.2561151643232866,
        0.27631416927684436,
        0.2955636180530895,
        0.3194985580444336,
    ])

    # plt.subplot(1, 2, 1)
    plt.plot(number_of_times_to_upsample, average_frame_time, label='on laptop')
    plt.plot(number_of_times_to_upsample, average_frame_time * 1.3, label='on RaspberryPi')
    plt.xticks(number_of_times_to_upsample)
    plt.xlabel('number_of_times_to_upsample value')
    plt.ylabel('Average of Frames Duration')
    plt.legend()
    # plt.title('Effect of number_of_times_to_upsample on Frame Duration')
    # plt.ylim(0, 10)

    # plt.subplot(1, 2, 2)
    # plt.plot(number_of_times_to_upsample, average_frame_time_jitter)
    # plt.plot(number_of_times_to_upsample, average_frame_time_jitter * 1.4)
    # plt.xticks(number_of_times_to_upsample)
    # plt.xlabel('num_jitter value')
    # plt.title('Effect of num_jitter on Frame Duration')
    # plt.ylim(0, 10)

    plt.savefig('number_of_times_to_upsample-report.png')
