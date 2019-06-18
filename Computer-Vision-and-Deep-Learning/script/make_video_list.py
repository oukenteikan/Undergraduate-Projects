with open('prefix.txt', 'r') as f:
    x = f.read()
x = x.splitlines()
for i in range(len(x)):
    x[i] = x[i][:94] + x[i][96:-4]
with open('in_overlap.txt', 'w') as f:
    for i in range(len(x) - 16):
        if (int(x[i][-6:]) % 8 == 1) and (int(x[i + 16][-6:]) > int(x[i][-6:])):
            f.write(x[i][:-6])
            f.write(' ' + str(int(x[i][-6:])) + ' 0')
            f.write('\n')

