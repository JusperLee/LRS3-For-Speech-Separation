'''
This part of the code is mainly to 
generate a txt file of mixed audio, 
the file format is: spk1 SDR spk2 SDR.
'''
import os
import random
import decimal


# step1: get all audio path
train_audio = []
val_audio = []
test_audio = []
path = '/data2/likai/AV-Model-lrs3/AV_data/raw_audio'
for root, dirs, files in os.walk(path):
    for file in files:
        if 'train' in root:
            train_audio.append(os.path.join(root, file))
        if 'test' in root:
            test_audio.append(os.path.join(root, file))
        if 'val' in root:
            val_audio.append(os.path.join(root, file))

random.shuffle(train_audio)
random.shuffle(test_audio)
random.shuffle(val_audio)
# step2: write path into file
tr_file = open('mix_2_spk_tr.txt', 'w')
cv_file = open('mix_2_spk_cv.txt', 'w')
tt_file = open('mix_2_spk_tt.txt', 'w')
# train data path
index = 1
repeat_path = []
audio_use = {}
train_audio_c = train_audio.copy()
while True:
    spk1 = random.choice(train_audio_c)
    spk2 = random.choice(train_audio_c)
    spk1_split = spk1.split('/')
    spk2_split = spk2.split('/')
    if spk1+spk2 not in repeat_path and spk2+spk1 not in repeat_path and spk1_split[-1].split('_')[0] != spk2_split[-1].split('_')[0]:
        snr_1 = float(decimal.Decimal(random.randrange(0, 500000))/decimal.Decimal(100000))
        snr_2 = -snr_1
        line = spk1 + ' ' + str(snr_1) + ' ' + spk2 + ' ' + str(snr_2) + '\n'

        if spk1 not in audio_use.keys():
            audio_use[spk1] = 1
        if spk2 not in audio_use.keys():
            audio_use[spk2] = 1
        if spk1 in audio_use.keys():
            if audio_use[spk1] == 6:
                train_audio_c.remove(spk1)
                continue
            if audio_use[spk1] != 6:
                if audio_use[spk2] != 6:
                    audio_use[spk1] += 1
                if audio_use[spk2] == 6:
                    train_audio_c.remove(spk2)
                    continue
        if spk2 in audio_use.keys():
            if audio_use[spk2] != 6:
                audio_use[spk2] += 1

        tr_file.write(line)
        repeat_path.append(spk1+spk2)
        repeat_path.append(spk2+spk1)
        print('\r {}'.format(index), end='')
        index += 1
    if index == 50001:
        print('\n')
        break

tr_file.close()

# validation data path
index = 1
repeat_path = []
audio_use = {}
val_audio_c = val_audio.copy()
while True:
    spk1 = random.choice(val_audio_c)
    spk2 = random.choice(val_audio_c)
    spk1_split = spk1.split('/')
    spk2_split = spk2.split('/')
    if spk1+spk2 not in repeat_path and spk2+spk1 not in repeat_path and spk1_split[-1].split('_')[0] != spk2_split[-1].split('_')[0]:
        snr_1 = float(decimal.Decimal(random.randrange(0, 500000))/decimal.Decimal(100000))
        snr_2 = -snr_1
        line = spk1 + ' ' + str(snr_1) + ' ' + spk2 + ' ' + str(snr_2) + '\n'

        if spk1 not in audio_use.keys():
            audio_use[spk1] = 1
        if spk2 not in audio_use.keys():
            audio_use[spk2] = 1
        if spk1 in audio_use.keys():
            if audio_use[spk1] == 8:
                val_audio_c.remove(spk1)
                continue
            else:
                if audio_use[spk2] != 8:
                    audio_use[spk1] += 1
                else:
                    val_audio_c.remove(spk2)
                    continue
        if spk2 in audio_use.keys():
            if audio_use[spk2] != 8:
                audio_use[spk2] += 1

        cv_file.write(line)
        repeat_path.append(spk1+spk2)
        repeat_path.append(spk2+spk1)
        print('\r {}'.format(index), end='')
        index += 1
    if index == 5001:
        print('\n')
        break

cv_file.close()

# test data path
index = 1
repeat_path = []
audio_use = {}
test_audio_c = test_audio.copy()
while True:
    spk1 = random.choice(test_audio_c)
    spk2 = random.choice(test_audio_c)
    spk1_split = spk1.split('/')
    spk2_split = spk2.split('/')
    if spk1+spk2 not in repeat_path and spk2+spk1 not in repeat_path and spk1_split[-1].split('_')[0] != spk2_split[-1].split('_')[0]:
        snr_1 = float(decimal.Decimal(random.randrange(0, 500000))/decimal.Decimal(100000))
        snr_2 = -snr_1
        line = spk1 + ' ' + str(snr_1) + ' ' + spk2 + ' ' + str(snr_2) + '\n'

        if spk1 not in audio_use.keys():
            audio_use[spk1] = 1
        if spk2 not in audio_use.keys():
            audio_use[spk2] = 1
        if spk1 in audio_use.keys():
            if audio_use[spk1] == 22:
                test_audio_c.remove(spk1)
                continue
            else:
                if audio_use[spk2] != 22:
                    audio_use[spk1] += 1
                else:
                    test_audio_c.remove(spk2)
                    continue
        if spk2 in audio_use.keys():
            if audio_use[spk2] != 22:
                audio_use[spk2] += 1

        tt_file.write(line)
        repeat_path.append(spk1+spk2)
        repeat_path.append(spk2+spk1)
        print('\r {}'.format(index), end='')
        index += 1
    if index == 3001:
        print('\n')
        break

tt_file.close()
