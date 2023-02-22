import matplotlib.pyplot as plt
import pandas as pd
from sklearn import decomposition
import os
import glob
import cv2
from tqdm import tqdm
from services.face_recognition import face_encodings, face_locations, face_distance, compare_faces


def grouped(iterable, n):
    return zip(*[iter(iterable)] * n)


if __name__ == '__main__':
    _face_encoding = []
    images_path = glob.glob(os.path.join('../../data/images/', '*.*'))
    images_path.sort()
    for img_path in tqdm(images_path):
        img = cv2.imread(img_path)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            _face_encoding.append(face_encodings(rgb_img)[0])
        except IndexError:
            pass
    df = pd.DataFrame(_face_encoding)
    print('original data frame')
    print(df)
    pca = decomposition.PCA(n_components=2)
    principal_components = pca.fit_transform(df)
    pca_data = pd.DataFrame(data=principal_components, columns=['x', 'y'])

    print('PCA (2D)')
    print(pca_data)
    plt.rcParams['figure.figsize'] = (6, 6)

    for i in range(len(pca_data) // 2):
        plt.scatter([pca_data['x'][2 * i], pca_data['x'][2 * i + 1]], [pca_data['y'][2 * i], pca_data['y'][2 * i + 1]],
                    label=images_path[2 * i].split('_')[0].split('/')[-1])
    plt.legend()
    plt.title('principal component analysis (2d)'.title())
    plt.savefig('principal_component_analysis_2d_report.png')

    pca3 = decomposition.PCA(n_components=3)
    principal_components3 = pca3.fit_transform(df)
    pca_data3 = pd.DataFrame(data=principal_components3, columns=['x', 'y', 'z'])

    print('PCA (3D)')
    print(pca_data3)
    fig = plt.figure(figsize=(6, 6))
    ax = plt.axes(projection="3d")
    for i in range(len(pca_data3) // 2):
        ax.scatter3D([pca_data3['x'][2 * i], pca_data3['x'][2 * i + 1]], [pca_data3['y'][2 * i], pca_data3['y'][2 * i + 1]],
                     [pca_data3['z'][2 * i], pca_data3['z'][2 * i + 1]],
                    label=images_path[2 * i].split('_')[0].split('/')[-1])
    plt.legend()
    plt.title('principal component analysis (3d)'.title())
    plt.savefig('principal_component_analysis_3d_report.png')
