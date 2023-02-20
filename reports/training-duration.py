import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    average_frame_time = [
        10, 4.234375,
        10, 2.94358974358974,
        10, 0.57788944723617,
        99.07562189054727,
        9, 2.63425925925925,
    ]
    image_count = np.arange(20) + 1
    plt.rcParams['figure.figsize'] = (6, 6)
    fig = plt.figure()
    plt.title('Effect of Image Compression on Model Training Duration')

    gray_compressed = [0.05910315, 0.07154415, 0.10547223, 0.1295165, 0.15304841, 0.19893278
        , 0.20187153, 0.2268315, 0.25750829, 0.26449152, 0.30792256, 0.3316004
        , 0.3270614, 0.36232356, 0.37705133, 0.44202646, 0.46010901, 0.49542899
        , 0.50005804, 0.52446718]
    compressed = [0.084689, 0.09333309, 0.1442064, 0.15199582, 0.20341902, 0.19586656
        , 0.23209345, 0.26256389, 0.31298385, 0.31784883, 0.39922204, 0.4285574
        , 0.44732474, 0.44039167, 0.48941662, 0.52686064, 0.53010122, 0.54707285
        , 0.57880902, 0.65246248]
    gray = [0.30836028, 0.51177628, 0.54029989, 0.84117539, 1.00285971, 1.03032539
        , 1.23832556, 1.43001782, 1.51801829, 1.83567062, 1.95442075, 2.09681907
        , 2.16964443, 2.34370216, 2.69342139, 2.74873294, 2.91438133, 3.19559044
        , 3.34849002, 3.44765891]
    original = [0.46408717, 0.70138387, 1.03248043, 1.01079329, 1.54507282, 1.73297118
        , 1.85820205, 2.1616437, 2.4016425, 2.60021712, 2.77988478, 3.19617202
        , 3.56404889, 3.75279806, 3.79770796, 4.00448917, 4.52822489, 4.62985499
        , 4.77047183, 5.03938307]

    plt.plot(image_count, gray_compressed, color='#2a9d8f', label='64x64px Grayscale Images')
    plt.plot(image_count, compressed, color='#e9c46a', label='64x64px Images with Original Colors')
    plt.plot(image_count, gray, color='#f4a261', label='Grayscale Images with Original Resolutions')
    plt.plot(image_count, original, color='#e76f51', label='Images with Original Colors and Resolutions')
    plt.legend()
    plt.xticks(image_count)
    plt.xlabel('Number of Images')
    plt.ylabel('Training Model Duration')
    plt.savefig('training-duration-report.png')
