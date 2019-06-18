import pandas as pd
import numpy as np
from scipy import interpolate
train=pd.read_csv("C:/Users/lenovo/Documents/WeChat Files/Appreciate-the-dusk/Files/HisRawData(1)/fan6_train.csv")
test=pd.read_csv("C:/Users/lenovo/Documents/WeChat Files/Appreciate-the-dusk/Files/HisRawData(1)/test.csv")



f=interpolate.UnivariateSpline(train['stime'], train['speed'])
test['speed']=f(test['stime'])
a=test['speed'].loc[0]
[x,y]=train.shape
train.loc[x]=[4,1,0,a,0]
f=interpolate.interp1d(train['stime'], train['speed'])
test['speed']=f(test['stime'])


