'''
The code is to get the audio in the 
video and downsample it to 16Khz.
'''
import os
import subprocess
from tqdm import tqdm
# Setting audio Parameters
sr = 16000 # sample rate
start_time = 0.0 # cut start time
length_time = 2.0 # cut audio length
outpath = '../raw_audio'
os.makedirs(outpath, exist_ok=True)


train_mouth = []
val_mouth = []
test_mouth = []
train = open('../train.txt', 'r').readlines()
test = open('../test.txt', 'r').readlines()
val = open('../val.txt', 'r').readlines()
for l in tqdm(train):
    l = l.replace('\n','')
    train_mouth.append(l)

for l in tqdm(val):
    l = l.replace('\n','')
    val_mouth.append(l)

for l in tqdm(test):
    l = l.replace('\n','')
    test_mouth.append(l)

with open('../video_process/video_path.txt', 'r') as f:
    lines = f.readlines()
    for line in tqdm(lines):
        if line != "":
            line = line.replace('\n','')
            l = line.split('/')[-2]+'_'+line.split('/')[-1].split('.')[0]
            if l in train_mouth:
                path = outpath+"/train"
                os.makedirs(path, exist_ok=True)
                command = ""
                command += 'ffmpeg -i {} -f wav -ar {} -ac 1 {}/tmp_{}.wav;'.format(line, sr, path, l)
                command += 'sox {}/tmp_{}.wav {}/{}.wav trim {} {};'.format(path, l, path, l, start_time, length_time)
                command += 'rm {}/tmp_{}.wav;'.format(path, l)
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.wait()
            if l in test_mouth:
                path = outpath+"/test"
                os.makedirs(path, exist_ok=True)
                command = ""
                command += 'ffmpeg -i {} -f wav -ar {} -ac 1 {}/tmp_{}.wav;'.format(line, sr, path, l)
                command += 'sox {}/tmp_{}.wav {}/{}.wav trim {} {};'.format(path, l, path, l, start_time, length_time)
                command += 'rm {}/tmp_{}.wav;'.format(path, l)
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.wait()
            if l in val_mouth:
                path = outpath+"/val"
                os.makedirs(path, exist_ok=True)
                command = ""
                command += 'ffmpeg -i {} -f wav -ar {} -ac 1 {}/tmp_{}.wav;'.format(line, sr, path, l)
                command += 'sox {}/tmp_{}.wav {}/{}.wav trim {} {};'.format(path, l, path, l, start_time, length_time)
                command += 'rm {}/tmp_{}.wav;'.format(path, l)
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.wait()
        else:
            pass
