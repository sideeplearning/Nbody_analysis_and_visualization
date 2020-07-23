#library

import random, cv2, os, sys, shutil, glob
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt


def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

if __name__ == '__main__':
    # demo_videos
    path = Path(r'C:\Users\user\Desktop\Nbody_analysis_and_visualization\output_jpg')
    rel_path = os.path.relpath(path) + '/*'
    print(rel_path)

    img_list = []
    file_path_list = []
    idx_ = -1
    for txt_path in glob.glob(rel_path):
        idx_ += 1
        file_name = os.path.splitext(os.path.basename(txt_path))[0]
        print(idx_, txt_path, file_name)
        file_path_list.append(txt_path)
        img_list.append(file_name)

    img_list = [int(s) for s in img_list]
    print(sorted(img_list))

    # path = Path(r'C:\Users\Si\Desktop\C++\Nbody_simulation\Nbody_simulator\Nbody_simulator\output_txt')

    img_path_time_series_list = []
    for idx, txt_name in enumerate(sorted(img_list)):
        print(idx, txt_name)

        rel_path = os.path.relpath(path)

        path_time_series = rel_path + '/' + str(txt_name) + ".png"
        print(path_time_series)
        img_path_time_series_list.append(path_time_series)

    img_list = []
    # path = './output_jpg/'
    for p in img_path_time_series_list:
        print('path:', p)
        file_num = os.path.splitext(os.path.basename(p))[0]
        file_num = int(file_num)
        print(file_num)
        skip = 5
        if file_num % skip == 0:
            img = cv2.imread(p)
            img_list.append(img)
            # print(len(os.listdir(path)))

    img_list[0].shape

    h = img_list[0].shape[0]
    w = img_list[0].shape[1]
    print(w, h)

    output_dir = './output_videos/'
    my_makedirs(output_dir)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    write_fps = 30

    out = cv2.VideoWriter(
        './output_videos/demo_video_skip' + str(skip) + '_fps_' + str(write_fps) + '.mp4',
        fourcc,
        write_fps,
        (w, h))

    for idx in range(len(img_list)):
        # print(img_list[idx])
        out.write(img_list[idx])
    print('output_videos_completed')