'''
   reading image file to npz file
'''

import numpy as np
import os
import cv2
from tqdm import tqdm


root = '../mouth'
save_path = '../npz'
#save_path = './'
os.makedirs(save_path, exist_ok=True)
mouth = open('valid_mouth.txt', 'r').readlines()
if_use_mouth = True # if use mouth image(True: use mouth, False: use frames)
# get valid mouth file
valid_mouth = []
for m in mouth:
    m = m.replace('\n', '').split('_')
    m = m[0]+'_'+m[1]
    valid_mouth.append(m)

train_mouth = []
val_mouth = []
test_mouth = []
train = open('../train.txt', 'r').readlines()
test = open('../test.txt', 'r').readlines()
val = open('../val.txt', 'r').readlines()

for l in tqdm(train):
    train_mouth.append(l.replace('\n',''))

for l in tqdm(test):
    test_mouth.append(l.replace('\n',''))

for l in tqdm(val):
    val_mouth.append(l.replace('\n',''))

folder = os.listdir(root)
#folder = ['00039_true']
mean = 0
std = 0
index = 0
for f in tqdm(folder):
    if f in train_mouth:
        path = os.path.join(root, f)
        frames = []
        for i in range(1, 51):
            img_path = os.path.join(path, "{:02d}.png".format(i))
            img = cv2.imread(img_path, 0)
            img = img / 255
            frames.append(img)
            m, s = cv2.meanStdDev(img) # m: mean, s:std
            mean += float(m)
            std += float(s)
            index += 1
        frames = np.array(frames)
        os.makedirs(os.path.join(save_path, 'train'),exist_ok=True)
        np.savez(os.path.join(save_path, 'train', '{}.npz'.format(f)), data=frames)
   
    if f in test_mouth:
        path = os.path.join(root, f)
        frames = []
        for i in range(1, 51):
            img_path = os.path.join(path, "{:02d}.png".format(i))
            img = cv2.imread(img_path, 0)
            img = img / 255
            frames.append(img)
            m, s = cv2.meanStdDev(img) # m: mean, s:std
            mean += float(m)
            std += float(s)
            index += 1
        frames = np.array(frames)
        os.makedirs(os.path.join(save_path, 'test'),exist_ok=True)
        np.savez(os.path.join(save_path, 'test', '{}.npz'.format(f)), data=frames)

    if f in val_mouth:
        path = os.path.join(root, f)
        frames = []
        for i in range(1, 51):
            img_path = os.path.join(path, "{:02d}.png".format(i))
            img = cv2.imread(img_path, 0)
            img = img / 255
            frames.append(img)
            m, s = cv2.meanStdDev(img) # m: mean, s:std
            mean += float(m)
            std += float(s)
            index += 1
        frames = np.array(frames)
        os.makedirs(os.path.join(save_path, 'val'),exist_ok=True)
        np.savez(os.path.join(save_path, 'val', '{}.npz'.format(f)), data=frames)


print('mean: {:06f}, std: {:06f}'.format(mean/index, std/index))