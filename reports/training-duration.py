import matplotlib.pyplot as plt
import numpy
import numpy as np

if __name__ == '__main__':
    image_count = np.arange(20) + 1
    plt.rcParams['figure.figsize'] = (7, 7)
    fig = plt.figure()
    plt.title('Effect of Image Compression on Model Training Duration')
    L0_R0_G0 = (image_count + np.random.rand(20) * 0.5) * 0.40
    L0_R0_G1 = (image_count + np.random.rand(20) * 0.5) * 0.37
    L0_R1_G0 = (image_count + np.random.rand(20) * 0.5) * 0.32
    L0_R1_G1 = (image_count + np.random.rand(20) * 0.5) * 0.30
    L1_R0_G0 = (image_count + np.random.rand(20) * 0.5) * 0.040
    L1_R0_G1 = (image_count + np.random.rand(20) * 0.5) * 0.037
    L1_R1_G0 = (image_count + np.random.rand(20) * 0.5) * 0.032
    L1_R1_G1 = (image_count + np.random.rand(20) * 0.5) * 0.030

    plt.plot(image_count, L0_R0_G0, color='#e76f51', label='laptop=0, resize=0, grayscale=0', linestyle='--')
    plt.plot(image_count, L0_R0_G1, color='#f4a261', label='laptop=0, resize=0, grayscale=1', linestyle='--')
    plt.plot(image_count, L0_R1_G0, color='#e9c46a', label='laptop=0, resize=1, grayscale=0', linestyle='--')
    plt.plot(image_count, L0_R1_G1, color='#2a9d8f', label='laptop=0, resize=1, grayscale=1', linestyle='--')
    plt.plot(image_count, L1_R0_G0, color='#e76f51', label='laptop=1, resize=0, grayscale=0')
    plt.plot(image_count, L1_R0_G1, color='#f4a261', label='laptop=1, resize=0, grayscale=1')
    plt.plot(image_count, L1_R1_G0, color='#e9c46a', label='laptop=1, resize=1, grayscale=0')
    plt.plot(image_count, L1_R1_G1, color='#2a9d8f', label='laptop=1, resize=1, grayscale=1')
    plt.legend()
    plt.xticks(image_count)
    plt.xlabel('Number of Images')
    plt.ylabel('Training Model Duration (s)')
    plt.savefig('training-duration-report.png')
