from tqdm import tqdm

file = open('mix_2_spk_tt.txt', 'r').readlines()

index = []

for line in file:
    line = line.split(' ')
    s1 = line[0].split('/')[-1]
    s2 = line[2].replace('\n','').split('/')[-1]
    if s1 not in index:
        index.append(s1)
    if s2 not in index:
        index.append(s2)


print(len(index))