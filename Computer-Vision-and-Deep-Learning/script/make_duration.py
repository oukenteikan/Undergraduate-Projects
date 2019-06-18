import os
with open('z.txt', 'r') as f:
    x = f.read()
x = x.splitlines()
cmd = 'ffmpeg -i {}.mp4 2>&1 | grep \'Duration\' | cut -d \' \' -f 4 | sed s/,//'
for i in x:
#    print(cmd.format(i))
    y = os.popen(cmd.format(i))
    z = y.read()
    y.close()
    z = z.split(':')
    a = float(z[1]) * 60 + float(z[2])
    print(i)
    print(a)
    with open ('Durations.txt', 'a') as f:
        f.write(i)
        f.write(' ')
        f.write(str(a))
        f.write('\n')
