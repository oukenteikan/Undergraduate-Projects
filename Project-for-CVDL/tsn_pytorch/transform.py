with open("test_01.lst", 'r') as f:
    x = f.read()
x = x.splitlines()
for i in range(len(x)):
    x[i] = "/mnt/lustre/huangrenze/UCF101/UCF-101/" + x[i]
x = '\n'.join(x)
with open("test_02.lst", 'w') as f:
    f.write(x)
