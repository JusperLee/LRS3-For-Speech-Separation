import cv2
import os
import matplotlib.pyplot as plt
import dlib
import numpy as np
from tqdm import tqdm
import subprocess
import face_recognition

def get_frames(pathlist, fps=25):
    # pathlist type list
    for path in tqdm(pathlist):
        index = path.split('/')[-2]+'_'+path.split('/')[-1].split('.')[0]
        os.makedirs('../frames/{}'.format(index), exist_ok=True)
        command = subprocess.Popen('ffmpeg -i {} -vf fps={} ../frames/{}/%02d.png;'.format(
            path, fps, index), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        command.wait()


def detect_mouth(inpath, outpath,  fps=25, time=2):
    '''
       inpath: file path of frames
       outpath: file path of mouth
       fps: video fps
       time: video time
    '''
    # Dlib requirements.
    #predictor_path = '../mouth_detector/shape_predictor_68_face_landmarks.dat'
    #detector = dlib.get_frontal_face_detector()
    #predictor = dlib.shape_predictor(predictor_path)

    #  folders getting
    folder = os.listdir(inpath)
    #folder = ['1']
    for f in tqdm(folder):
        # Required parameters for mouth extraction.
        width_crop_max = 0
        height_crop_max = 0
        index = 1
        while True:
            path = os.path.join(inpath, f, '{:02d}.png'.format(index))

            # Load the jpg file into a numpy array
            image = face_recognition.load_image_file(path)
            face_locations = face_recognition.face_locations(
                image, number_of_times_to_upsample=0, model="cnn")
            # Find all facial features in all the faces in the image
            face_landmarks_list = face_recognition.face_landmarks(
                image, face_locations=face_locations)
            if len(face_locations) == 0:
                break
            # mkdir path
            os.makedirs(os.path.join(outpath, f), exist_ok=True)
            frame = cv2.imread(path)
            h, w, _ = frame.shape
            # 20 mark for mouth
            marks = np.zeros((2, 24))
            for face_landmarks in face_landmarks_list:
                # Print the location of each facial feature in this image
                co = 0
                for facial_feature in face_landmarks.keys():
                    if facial_feature == 'top_lip':
                        lip = face_landmarks[facial_feature]
                        for i in lip:
                            marks[0, co] = i[0]
                            marks[1, co] = i[1]
                            co += 1
                    if facial_feature == 'bottom_lip':
                        lip = face_landmarks[facial_feature]
                        for i in lip:
                            marks[0, co] = i[0]
                            marks[1, co] = i[1]
                            co += 1
            # Get the extreme points(top-left & bottom-right)
            X_left, Y_left, X_right, Y_right = [int(np.amin(marks, axis=1)[0]), int(np.amin(marks, axis=1)[1]),
                                                int(np.amax(marks, axis=1)[0]),
                                                int(np.amax(marks, axis=1)[1])]
            # Find the center of the mouth.
            X_center = (X_left + X_right) / 2.0
            Y_center = (Y_left + Y_right) / 2.0

            # Make a boarder for cropping.
            border = 30
            X_left_new = X_left - border
            Y_left_new = Y_left - border
            X_right_new = X_right + border
            Y_right_new = Y_right + border

            # Width and height for cropping(before and after considering the border).
            width_new = X_right_new - X_left_new
            height_new = Y_right_new - Y_left_new
            width_current = X_right - X_left
            height_current = Y_right - Y_left

            # Determine the cropping rectangle dimensions(the main purpose is to have a fixed area).
            if width_crop_max == 0 and height_crop_max == 0:
                width_crop_max = width_new
                height_crop_max = height_new
            else:
                width_crop_max += 1.5 * \
                    np.maximum(width_current - width_crop_max, 0)
                height_crop_max += 1.5 * \
                    np.maximum(height_current - height_crop_max, 0)

            # # # Uncomment if the lip area is desired to be rectangular # # # #
            #########################################################
            # Find the cropping points(top-left and bottom-right).
            X_left_crop = int(X_center - width_crop_max / 2.0)
            X_right_crop = int(X_center + width_crop_max / 2.0)
            Y_left_crop = int(Y_center - height_crop_max / 2.0)
            Y_right_crop = int(Y_center + height_crop_max / 2.0)

            if X_left_crop >= 0 and Y_left_crop >= 0 and X_right_crop < w and Y_right_crop < h:
                mouth = frame[Y_left_crop:Y_right_crop,
                    X_left_crop:X_right_crop, :]

                # Save the mouth area.
                mouth_gray = cv2.cvtColor(mouth, cv2.COLOR_BGR2GRAY)
                mouth_gray = cv2.resize(mouth_gray, (120, 120))
                cv2.imwrite(os.path.join(
                        outpath, f, "{:02d}.png".format(index)), mouth_gray)
            else:
                pass
            index += 1
            if index == 51:
                break


def resize_img(path, size):
    for root, dirs, files in tqdm(os.walk(path)):
        for file in files:
            if file.endswith('png'):
                f = os.path.join(root, file)
                img = cv2.imread(f)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img_gray = cv2.resize(img_gray, size)
                cv2.imwrite(f, img_gray)


def file_to_path(filename, root):
    lines = open(filename, 'r').readlines()
    filename_list = []
    for file in lines:
        file = file.replace('\n', '').split('_')
        filename_list.append(os.path.join(root, file[0], file[1]+'.mp4'))
    return filename_list

if __name__ == "__main__":
    video_path = 'valid_mouth.txt'
    pathlist = file_to_path(video_path, '../lrs3')
    inpath = '../frames'
    outpath = '../mouth'
    change_root = '../frames'
    print('-------------Getting video frames-------------')
    get_frames(pathlist)
    print('--------------Detection the mouth-------------')
    detect_mouth(inpath, outpath)
    print('--------------Resize the frames-------------')
    resize_img(change_root, (120, 120))
