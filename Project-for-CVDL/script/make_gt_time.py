import os

def rerank(path):
    files = os.listdir(path)
    s = {}
    for file in files:
        f = open(os.path.join(path, file))
        content = f.read().split()
        for i in range(len(content)):
            if i%3==0 :
                if s.has_key(content[i]):
                    s[content[i]].append((content[i+1], content[i+2]))
                else
                    s[content[i]] = [(content[i+1], content[i+2])]
    print ("total video %d" % len(s))
    count = 0
    for name in s:
        url = "http://crcv.ucf.edu/THUMOS14/test_set/TH14_test_set_mp4/" + name + ".mp4"
        filename = path + "/video/" + name + ".mp4"
        urlretrieve(url, filename)
        count += 1
        print ("now is video %d" % count)
    return True

finish = rerank("D:/Code/python/annotation")
print ("finish")