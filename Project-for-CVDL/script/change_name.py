with open('Durations.txt', 'r') as f:
    x = f.read()
x = x.splitlines()
for i in range(len(x)):
    if x[i].find('.mp4') != -1:
        x[i] = x[i][:x[i].find('.mp4')] + x[i][x[i].find('.mp4') + 4:]
        print(x[i])
    with open('Durations.txt', 'w') as f:
        f.write(x[i])
        f.write('\n')
