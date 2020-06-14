# Instruction for generating data

Following are the steps to generate training and testing data.  There are several parameters to change in order to match different purpose. 

We will release the benchmark of Speech-Separation on the LRS3 dataset as soon as possible.

Our script repository is to make the multi-modal speech separation task have a unified standard in data set generation. So that we can follow up on multi-modal speech separation tasks.

We hope that the LRS3 data set will have a unified generation standard for pure voice separation tasks like the WSJ0 data set.

:ballot_box_with_check: Our baseline model is coming soon!!!!!
## Requirement

- **ffmpeg 4.2.1**
- **sox 14.4.2**
- **numpy 1.17.2**
- **opencv-python 4.1.2.30**
- **librosa 0.7.0**
- **dlib 19.19.0**
- **face_recognition 1.3.0**

## Step 1 - Getting raw Data

1. In this method, we use the [Lip Reading Sentences 3 (LRS)](http://www.robots.ox.ac.uk/~vgg/data/lip_reading/lrs3.html) dataset as our training, validation, and test sets.

> Afouras T, Chung J S, Senior A, et al. Deep audio-visual speech recognition[J]. IEEE transactions on pattern analysis and machine intelligence, 2018.
2. We just use the train_val and test folders in the LRS3 dataset. These two folders need to be merged before using our script.
## Step 2 - Processing Video Data

1.  Open **./video_process/** 

```shell
cd video_process
```
2.  Then use the **video_process.py** script to get the video frame, get the image of the lip area, and finally adjust its size to 120 × 120.

```python
python video_process.py
# Change the path in the script to your data path.
video_path = 'valid_mouth.txt' # Collection of files with lips detected
inpath = '../frames' # save video frames path
outpath = '../mouth' # save mouth images path
change_root = '../frames' # resize the frames file path
# You can note this code first.
print('--------------Resize the frames-------------')
resize_img(change_root, (120, 120))
```

3. In order to process the image data faster, we use the following command to store the image data in the numpy data format ".npz".

```python
 python video_to_np.py
```

> This file is the lrs3 dataset txt file.

```python
train = open('../train.txt', 'r').readlines()
test = open('../test.txt', 'r').readlines()
val = open('../val.txt', 'r').readlines()
```

## Step 3 - Processing audio data

1. Running **audio_cut.py** code, you can cut the sound of the video through the sox software to get a 2s voice signal.

2. Mix it. We use -5db to 5db to mix the voices of two people. This part of the code refers to the method of [deep clustering](https://www.merl.com/demos/deep-clustering) data mixing.


```python
matlab -nodisplay -r create_wav_2speakers
#You need to change this part in create_wav_2speakers.m
'''
data_type = {'tr','cv','tt'};
wsj0root = ''; % YOUR_PATH/raw_audio
output_dir16k=''; % 16k path
output_dir8k=''; % 8k path
'''
```


## Then, you can start to training data.

## Citing Dataset Processing Script

If you find this repository useful, please cite it in your publications.

```latex
@misc{LRS3SS,
  author = {Kai Li},
  title = {LRS3-For-Speech-Separation},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/JusperLee/LRS3-For-Speech-Separation}},
}
```
