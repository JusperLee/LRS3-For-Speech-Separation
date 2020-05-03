file = open('mix_2_spk_tt.txt', 'r').readlines()

lines = []
for l in file:
    lines.append(l.replace('\n', ''))

non_same = []

for line in lines:
    line = line.split(' ')
    if line[0] not in non_same:
        non_same.append(line[0])
    if line[2] not in non_same:
        non_same.append(line[2])


print(len(non_same))