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
    for name in s:
        url = "http://crcv.ucf.edu/THUMOS14/Validation_set/videos/" + name + ".mp4"
        filename = path + "/video/" + name + ".mp4"
        urlretrieve(url, filename)
    return True

finish = download("D:/Code/python/annotation")