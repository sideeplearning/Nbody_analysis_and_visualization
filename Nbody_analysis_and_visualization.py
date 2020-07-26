

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

def move_glob(dst_path, pathname, recursive=True):
    i= 0
    for p in glob.glob(pathname, recursive=recursive):
        i+=1
        #shutil.move(p, dst_path)
        shutil.copy(p, dst_path)
        print('No.', i, 'sample has been transfered!')


def mat_plot(i, file_id, delta_iteration, x_list, y_list, num_galaxy_1, num_galaxy_2, year_current_frame):
    # シミュレーションの結果を入力
    # x_list = [float(s) for s in x_list[0:num_galaxy_1]]
    # y_list = [float(s) for s in y_list[0:num_galaxy_1]]

    x_list_g1 = [float(s) for s in x_list[:num_galaxy_1]]
    y_list_g1 = [float(s) for s in y_list[:num_galaxy_1]]
    x_g1 = np.array(x_list_g1)
    y_g1 = np.array(y_list_g1)

    x_list_g2 = [float(s) for s in x_list[num_galaxy_1:num_galaxy_1 + num_galaxy_2]]
    y_list_g2 = [float(s) for s in y_list[num_galaxy_1:num_galaxy_1 + num_galaxy_2]]
    x_g2 = np.array(x_list_g2)
    y_g2 = np.array(y_list_g2)


    fontsize_ = 25

    # 散布図を描画
    fig = plt.figure(figsize=(15, 15))

    ax = plt.gca()

    # please change plot color here!
    # background color white, star RGB
    ax.set_facecolor('w')
    color_list = ['blue', 'red']

    # background color white, star RGB
    #ax.set_facecolor('black')
    #color_list = ['white', 'white']

    plt.scatter(x_g1, y_g1, s=1, color=color_list[0], label="galaxy_01")
    plt.scatter(x_g2, y_g2, s=1, color=color_list[1], label="galaxy_02")

    plt.xlabel('x-axis', fontsize=fontsize_)
    plt.ylabel('y-axis', fontsize=fontsize_)
    plt.xlim(-30, +30)
    plt.ylim(-30, +30)

    # plt.colorbar(label='label')
    # plt.grid(True)
    # plt.legend(loc='upper left', fontsize=18)

    leg0 = plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=fontsize_)

    particle_num = ['Total_particle_num: ' + '\n' + str(num_galaxy_1 + num_galaxy_2)]
    leg1 = plt.legend(particle_num, loc='upper left', bbox_to_anchor=(1, 0.9), fontsize=fontsize_)

    particle_num_01 = [
        'Galaxy01_initial_num: ' + '\n' + str(num_galaxy_1) + '\n' + 'Galaxy02_initial_num: ' + '\n' + str(
            num_galaxy_2)]
    leg2 = plt.legend(particle_num_01, loc='upper left', bbox_to_anchor=(1, 0.80), fontsize=fontsize_)

    theta = ['BH_tree_theta:' + '\n' + ' 0.9']
    leg3 = plt.legend(theta, loc='upper left', bbox_to_anchor=(1, 0.6), fontsize=fontsize_)

    real_time = ['Time: ' + '\n' + str(i * year_current_frame) + '_years']
    leg4 = plt.legend(real_time, loc='upper left', bbox_to_anchor=(1, 0.5), fontsize=fontsize_)

    epoch = ['Frame_No.' + '\n' + str(i)]
    leg5 = plt.legend(epoch, loc='upper left', bbox_to_anchor=(1, 0.4), fontsize=fontsize_)

    field_view = ['Field_view: ' + '\n' + '30pc']
    leg6 = plt.legend(field_view, loc='upper left', bbox_to_anchor=(1, 0.3), fontsize=fontsize_)

    fig.add_artist(leg0)
    fig.add_artist(leg1)
    fig.add_artist(leg2)
    fig.add_artist(leg3)
    fig.add_artist(leg4)
    fig.add_artist(leg5)
    fig.add_artist(leg6)

    title_ = ("No." + str('_') + str(int(file_id)/delta_iteration))
    plt.title(title_, fontsize=fontsize_)
    Nbody_output_jpg = './output_jpg'
    my_makedirs(Nbody_output_jpg)

    filename = Nbody_output_jpg + "/" + str(file_id) + ".png"
    plt.savefig(filename, bbox_inches="tight")
    plt.close()


if __name__ == '__main__':
    # copy txt files from simulation output folder on D driver to the analysis folder on C driver
    try:
        dst_path = './output_txt'
        my_makedirs(dst_path)
        print(dst_path)
        move_glob(dst_path, 'D:\\Nbody simulation\\galaxy_simulator\\output_txt\\*.txt')

    except:
        print('output files already been transfered!')
        raise

    # setting simulation parameters
    size_galaxy_1 = 5
    size_galaxy_2 = 1
    ratio = size_galaxy_1 / (size_galaxy_1 + size_galaxy_2)
    print(ratio)

    # read simulation output txt files
    #path = Path(r'C:\Users\Si\Desktop\C++\Nbody_simulation\Nbody_simulator\Nbody_simulator\output_txt')
    path = Path(r'C:\Users\user\Desktop\Nbody_analysis_and_visualization\output_txt')

    rel_path = os.path.relpath(path) + '/*'
    print(rel_path)

    file_name_list1 = []
    idx_ = -1
    for txt_path in glob.glob(rel_path):
        idx_ += 1
        file_name = os.path.splitext(os.path.basename(txt_path))[0]
        print(idx_, txt_path, file_name)
        file_name_list1.append(file_name)

    # read images files already generated and compare with simulation output txt files
    # generate difference between these two folders of files, then only visulize the undone txt files into images
    # path = Path(r'C:\Users\Si\Desktop\C++\Nbody_simulation\Nbody_simulator\Nbody_simulator\output_txt')
    path2 = Path(r'C:\Users\user\Desktop\Nbody_analysis_and_visualization\output_jpg')
    rel_path2 = os.path.relpath(path2) + '/*'
    #print(rel_path)

    file_name_list2 = []
    idx_ = -1
    for txt_path in glob.glob(rel_path2):
        idx_ += 1
        file_name = os.path.splitext(os.path.basename(txt_path))[0]
        print(idx_, txt_path, file_name)
        file_name_list2.append(file_name)

    set1 = set(file_name_list1)
    set2 = set(file_name_list2)
    print(len(file_name_list1), len(file_name_list2))

    file_name_list = list(set1.difference(set2))
    print(file_name_list)



    # sort txt by time-series
    file_name_list = [int(s) for s in file_name_list]
    path_time_series_list = []
    for idx, txt_name in enumerate(sorted(file_name_list)):
        #print(idx, txt_name)

        rel_path = os.path.relpath(path)

        path_time_series = rel_path + '/' + str(txt_name) + ".txt"
        print(path_time_series)
        path_time_series_list.append(path_time_series)


    # calculate delta_iteration
    delta_iteration_list = []
    for index in range(2):
        print(index)

        # read the prediction text files
        txt_files = path_time_series_list
        delta_iteration = os.path.splitext(os.path.basename(txt_files[index]))[0]
        delta_iteration = int(delta_iteration)
        delta_iteration_list.append(delta_iteration)

    delta_iteration = delta_iteration_list[1]-delta_iteration_list[0]
    print('delta_iteration:', delta_iteration)
    print(len(path_time_series_list))

    year_per_iteration = 100
    year_current_frame = year_per_iteration * delta_iteration
    print('year_current_frame:', year_current_frame)

    # extract txt files cordinates and visualize it using matplotlib
    for index, delta_file_path in enumerate(path_time_series_list):
        print(index, delta_file_path)
        # txt file id
        file_id = os.path.splitext(os.path.basename(delta_file_path))[0]

        # read the prediction text files
        txt_files = path_time_series_list

        fileobj = open(txt_files[index], "r", encoding="utf_8")
        print('fileobj', fileobj)

        boxes_list = []
        row_no = 0
        fileobj = open(txt_files[index], "r", encoding="utf_8")
        while True:
            line = fileobj.readline()
            if line:
                row_no += 1
                boxes_list.append(line)
                # print(row_no, ":", line)
            else:
                break

        boxes_list_selected = []
        # all
        for i in range(len(boxes_list)):
            # top10
            # for i in range(10):
            boxes_list_split = boxes_list[i].split()
            # print(boxes_list_split)
            boxes_list_split[0] = boxes_list_split[0].split('\n', 1)[0]

            boxes_list_selected.append(boxes_list_split)

            # print(i, boxes_list_split)

        # print(len(boxes_list_selected), boxes_list_selected)
        x_list = []
        y_list = []
        for idx_, cord in enumerate(boxes_list_selected):
            cord = cord[0].split(',')
            x = cord[0]
            y = cord[1]
            v_x = cord[2]
            v_y = cord[3]
            # print(idx_,cord[0], cord[1], cord[2], cord[3])
            x_list.append(x)
            y_list.append(y)
            # print(cord_list)

        # visualization for every iteration

        num_galaxy_1 = int(len(x_list) * ratio)
        # print(num_galaxy_1)

        num_galaxy_2 = len(x_list) - num_galaxy_1
        # print(num_galaxy_2)

        mat_plot(index, file_id, delta_iteration, x_list, y_list, num_galaxy_1, num_galaxy_2, year_current_frame)



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

    part = len(img_path_time_series_list)//3
    print(part)

    for i in range(1):
        img_path_time_series_part = img_path_time_series_list[:part]
        img_list = []
        # path = './output_jpg/'
        for p in img_path_time_series_part:
            print('index:', p)
            try:
                img = cv2.imread(p)
                img_list.append(img)
                # print(len(os.listdir(path)))
            except:
                print('too many images caused OpenCV memory_lick')
                pass

        img_list[0].shape

        h = img_list[0].shape[0]
        w = img_list[0].shape[1]
        print(w, h)
        '''
        output_dir = './output_videos/'
        my_makedirs(output_dir)
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        write_fps = 10
        
        out = cv2.VideoWriter(
            './output_videos/demo_video_fps_' + str(write_fps) + '.mp4',
            fourcc,
            write_fps,
            (w, h))

        for idx in range(len(img_list)):
            # print(img_list[idx])
            # out.write(img_list[idx])
            pass
        '''
        print('output_videos_completed')

