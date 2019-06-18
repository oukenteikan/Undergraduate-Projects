from urllib.request import urlretrieve
import os

def download(path):
    files = os.listdir(path)
    os.mkdir(path+"/video")
    s = set()
    for file in files:
        f = open(path + "/" + file)
        content = f.read().split()
        for i in range(len(content)):
            if i%3==0 :
                s.add(content[i])
    print ("total video %d" % len(s))
    count = 0
    for name in s:
        url = "http://crcv.ucf.edu/THUMOS14/test_set/TH14_test_set_mp4/" + name + ".mp4"
        filename = path + "/video/" + name + ".mp4"
        urlretrieve(url, filename)
        count += 1
        print ("now is video %d" % count)
    return True

finish = download("D:/Code/python/TH14_Temporal_annotations_test/TH14_Temporal_Annotations_Test/annotations/annotation")
print ("finish")