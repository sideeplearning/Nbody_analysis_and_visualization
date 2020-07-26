# library

import random, cv2, os, sys, shutil, glob
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
from moviepy.editor import *


def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)


if __name__ == '__main__':
    # parameters for mergeing the simulation output videos
    ## we divided all frames into a certai number of groups (num_of_division_ = 100), then merge them together
    ## this could avoid openCV memory lick during final_video generation.

    # differatial of iterations in the simulation, maintian same as Nbody_analysis_and_visualization.py
    delta_iteration_ = 10

    # how many piece of sub_videos want to generate
    ## num_of_division_ must be smaller than the length of sum(all frames)
    num_of_division_ = 100
    # how many frames want to skip during the generation of sub_videos
    ## skip_ must be smaller than the length of sum(each sub_videos' frame)
    skip_ = 10

    # writing fps
    write_fps_ = 30

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

    img_path_time_series_list = []
    for idx, txt_name in enumerate(sorted(img_list)):
        print(idx, txt_name)

        rel_path = os.path.relpath(path)

        path_time_series = rel_path + '/' + str(txt_name) + ".png"
        print(path_time_series)
        img_path_time_series_list.append(path_time_series)

    # num of division
    num_of_division = num_of_division_
    part = len(img_path_time_series_list) // num_of_division
    print(part)

    for i in range(num_of_division):
        try:
            img_path_time_series_part = img_path_time_series_list[part * i: part * (i + 1)]
            print('delta_part:', i, part * (i))
        except:
            img_path_time_series_part = img_path_time_series_list[part * i:]
            print('delta_part:', i, len(img_path_time_series_list) - part * (i))

        img_list = []
        # path = './output_jpg/'
        for p in img_path_time_series_part:
            # print('path:', p)
            file_num = os.path.splitext(os.path.basename(p))[0]
            file_num = int(file_num) / int(delta_iteration_)
            # print('file_num', file_num)
            skip = skip_
            if skip <= int(part):
                if file_num % skip == 0:
                    img = cv2.imread(p)
                    img_list.append(img)
                    # print(len(os.listdir(path))
            else:
                print('please input value of skip, which skip_ <= part')
                pass

        img_list[0].shape

        h = img_list[0].shape[0]
        w = img_list[0].shape[1]
        print(w, h)

        output_dir = './output_videos/'
        my_makedirs(output_dir)
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        write_fps = write_fps_

        out = cv2.VideoWriter(
            './output_videos' + '/' + str(i) + '.mp4',
            fourcc,
            write_fps,
            (w, h))

        for idx in range(len(img_list)):
            # print(img_list[idx])
            out.write(img_list[idx])

    # merge all demo_videos
    path = Path(r'C:\Users\user\Desktop\Nbody_analysis_and_visualization\output_videos')
    rel_path = os.path.relpath(path) + '/*'
    print(rel_path)

    vid_list = []
    file_path_list = []
    idx_ = -1
    for txt_path in glob.glob(rel_path):
        idx_ += 1
        file_name = os.path.splitext(os.path.basename(txt_path))[0]
        last_alpha = len(file_name) - 1
        print(idx_, txt_path, file_name[last_alpha])
        file_path_list.append(txt_path)
        vid_list.append(file_name[last_alpha])

    vid_list = [int(s) for s in vid_list]
    print(sorted(vid_list))

    vid_path_time_series_list = []
    for idx, txt_name in enumerate(sorted(vid_list)):
        print(idx, txt_name)

        rel_path = os.path.relpath(path)

        path_time_series = rel_path + '/' + str(idx) + '.mp4'
        print(path_time_series)
        vid_path_time_series_list.append(path_time_series)
    print('dummy')

    final_clip = concatenate_videoclips(
        [VideoFileClip(vid_path_time_series_list[ind_]) for ind_ in range(len(vid_list) - 1)], method="compose")

    final_clip.write_videofile("vid_merged.mp4")
    print('all subvideos merged except neglectng the last one')

print('output_videos_completed')
