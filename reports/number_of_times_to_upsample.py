import matplotlib.pyplot as plt
import numpy as np
import math

if __name__ == '__main__':
    average_frame_time = [
        99.61691542288557,
        172.9655172413793,
        474.30232558139534,
        1597.076923076923,
        5439.5,
    ]
    number_of_times_to_upsample = np.arange(5) + 1
    plt.rcParams['figure.figsize'] = (12, 6)
    fig = plt.figure()
    fig.suptitle('Effect of number_of_times_to_upsample on User Experience', fontsize=20)

    number_of_frames = [201, 116, 43, 13, 4]

    plt.subplot(1, 2, 1)
    plt.plot(number_of_times_to_upsample, average_frame_time)
    plt.xticks(number_of_times_to_upsample)
    plt.xlabel('number_of_times_to_upsample value')
    plt.ylabel('Average of Frames Duration in 20s')

    plt.subplot(1, 2, 2)
    plt.plot(number_of_times_to_upsample, number_of_frames)
    plt.xticks(number_of_times_to_upsample)
    plt.xlabel('number_of_times_to_upsample value')
    plt.ylabel('Number of Total Frames in 20s')

    plt.savefig('number_of_times_to_upsample-report.png')
