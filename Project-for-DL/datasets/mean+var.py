import numpy as np
from PIL import Image
import os
rootdir = './data_large'
list = os.listdir(rootdir) 
mean0=0
var0=0
mean1=0
var1=0
mean2=0
var2=0
for i in range(0,len(list)):
	path = os.path.join(rootdir,list[i])
	im = Image.open(path)
	im=im.resize((256, 256))
	im.save(path)

	# mean0=mean0+ np.mean(im2[:,:,0])
	# var0=var0+np.var(im2[:,:,0])
	# mean1=mean1+ np.mean(im2[:,:,1])
	# var1=var1+np.var(im2[:,:,1])
	# mean2=mean2+ np.mean(im2[:,:,2])
	# var2=var2+np.var(im2[:,:,2])
	if(i%1000==0):
		print(i)
# mean0=mean0/len(list)
# std0=np.sqrt(var0/len(list))
# mean1=mean1/len(list)
# std1=np.sqrt(var1/len(list))
# mean2=mean2/len(list)
# std2=np.sqrt(var2/len(list))
# print('mean0=',mean0)
# print('mean1=',mean1)
# print('mean2=',mean2)
# print('std0=',std0)
# print('std1=',std1)
# print('std2=',std2)