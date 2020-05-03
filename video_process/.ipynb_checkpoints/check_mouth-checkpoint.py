'''
Check if all mouths contain 50 frames.
'''

import os
from tqdm import tqdm
file = open('valid_mouth.txt', 'w')
mouth = '../mouth'
folder = os.listdir(mouth)
for f in tqdm(folder):
    flag = True
    for i in range(1, 51):
        fi = os.path.join(mouth, f, '{:02d}.png').format(i)
        if not os.path.exists(fi):
            flag = False
    
    if flag:
        file.write(str(f)+'\n')
    else:
        pass
file.close()
