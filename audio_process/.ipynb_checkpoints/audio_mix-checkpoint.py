import os
import librosa
import numpy as np
from tqdm import tqdm
data_type = ['tr', 'cv', 'tt']
dataroot = '../raw_audio'
output_dir16k = '../audio_mouth/2speakers/wav16k'
output_dir8k = '../audio_mouth/2speakers/wav8k'

# create data path
for i_type in data_type:
    # 16k
    os.makedirs(os.path.join(output_dir16k, i_type, 's1'), exist_ok=True)
    os.makedirs(os.path.join(output_dir16k, i_type, 's2'), exist_ok=True)
    os.makedirs(os.path.join(output_dir16k, i_type, 'mix'), exist_ok=True)
    s1_16k_path = os.path.join(output_dir16k, i_type, 's1')
    s2_16k_path = os.path.join(output_dir16k, i_type, 's2')
    mix_16k_path = os.path.join(output_dir16k, i_type, 'mix')
    # 8k
    os.makedirs(os.path.join(output_dir8k, i_type, 's1'), exist_ok=True)
    os.makedirs(os.path.join(output_dir8k, i_type, 's2'), exist_ok=True)
    os.makedirs(os.path.join(output_dir8k, i_type, 'mix'), exist_ok=True)
    s1_8k_path = os.path.join(output_dir8k, i_type, 's1')
    s2_8k_path = os.path.join(output_dir8k, i_type, 's2')
    mix_8k_path = os.path.join(output_dir8k, i_type, 'mix')
    # open file
    file = open('mix_2_spk_'+i_type+'.txt', 'r')
    lines = file.readlines()
    sr8k = 8000
    sr16k = 16000
    for line in tqdm(lines):
        if line != '':
            line = line.replace('\n', '').split(' ')
            spk1 = line[0]
            spk2 = line[2]
            snr1 = float(line[1])
            snr2 = float(line[3])
            mix_name = spk1.split(
                '/')[-1].split('.')[0]+'_'+str(snr1)+'_'+spk2.split('/')[-1].split('.')[0]+'_'+str(snr2)+'.wav'
            # reading audio
            s1_8k, _ = librosa.load(spk1, sr8k)
            s2_8k, _ = librosa.load(spk2, sr8k)
            s1_16k, _ = librosa.load(spk1, sr16k)
            s2_16k, _ = librosa.load(spk2, sr16k)
            # getting weight
            weight_1 = np.power(10, snr1/20)
            weight_2 = np.power(10, snr2/20)
            # weight * audio
            s1_8k = weight_1 * s1_8k
            s2_8k = weight_2 * s2_8k
            s1_16k = weight_1 * s1_16k
            s2_16k = weight_2 * s2_16k
            # mix audio
            mix_8k = s1_8k + s2_8k
            mix_16k = s1_16k + s2_16k
            # save audio
            librosa.output.write_wav(os.path.join(s1_8k_path, mix_name), s1_8k, sr8k)
            librosa.output.write_wav(os.path.join(s2_8k_path, mix_name), s2_8k, sr8k)
            librosa.output.write_wav(os.path.join(mix_8k_path, mix_name), mix_8k, sr8k)
            librosa.output.write_wav(os.path.join(s1_16k_path, mix_name), s1_16k, sr16k)
            librosa.output.write_wav(os.path.join(s2_16k_path, mix_name), s2_16k, sr16k)
            librosa.output.write_wav(os.path.join(mix_16k_path, mix_name), mix_16k, sr16k)
        else:
            pass

