import random
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import pandas as pd
import numpy as np
import missingno as msno
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix
from sklearn import svm
import sklearn.tree as tree
class Smote:
    def __init__(self,samples,N=10,k=5):
        self.n_samples,self.n_attrs=samples.shape
        self.N=N
        self.k=k
        self.samples=samples
        self.newindex=0
       # self.synthetic=np.zeros((self.n_samples*N,self.n_attrs))

    def over_sampling(self):
        N=int(self.N/100)
        self.synthetic = np.zeros((self.n_samples * N, self.n_attrs))
        neighbors=NearestNeighbors(n_neighbors=self.k).fit(self.samples)
        print('neighbors',neighbors)
        for i in range(len(self.samples)):
            nnarray=neighbors.kneighbors(self.samples[i].reshape(1,-1),return_distance=False)[0]
            #print nnarray
            self._populate(N,i,nnarray)
        return self.synthetic


    # for each minority class samples,choose N of the k nearest neighbors and generate N synthetic samples.
    def _populate(self,N,i,nnarray):
        for j in range(N):
            nn=random.randint(0,self.k-1)
            dif=self.samples[nnarray[nn]]-self.samples[i]
            gap=random.random()
            self.synthetic[self.newindex]=self.samples[i]+gap*dif
            self.newindex+=1

for y in range(5):
    y=0
    data=pd.read_csv(str(y+1)+'year_withoutmiss.csv',header=None,na_values='?')
    data = data[(data[64] == 0) | (data[64] == 1)]
    data1 = data[data[64] == 1]
    data0=data[data[64]==0]
    trainx1, testx1, trainy1, testy1 = train_test_split(data1.iloc[:, 0:64], data1[64], test_size=0.25)
    trainx0, testx0, trainy0, testy0 = train_test_split(data0.iloc[:, 0:64], data0[64], test_size=0.25)
    testx=pd.concat([pd.DataFrame(testx1),pd.DataFrame(testx0)])
    testy=pd.concat([pd.DataFrame(testy1),pd.DataFrame(testy0)])
    trainy1=pd.DataFrame(trainy1)
    trainx1=np.array(trainx1)
    s=Smote(trainx1,N=2500)
    trainx1new=pd.DataFrame(s.over_sampling())
    trainx1=pd.DataFrame(trainx1)
    trainx=pd.concat([trainx0,trainx1,trainx1new])
    newy=pd.DataFrame(np.zeros(trainx1new.shape[0]))
    newy.columns = [64]
    newy[64]=1
    trainy0=pd.DataFrame(trainy0)
    trainy=pd.concat([trainy0,trainy1,newy])
    trainx=trainx.drop([0,
1,
49,
51,
9,
16,
62,
13,
11,
6,
17,
46,
7,
42,
34,
55,
61,
3,
18,
29,
53,
                        47,
                        27,
                        2,
                        44,
                        48,
                        35,
                        56,
                        52,
                        30,
                        19,
                        15,
                        32,
                        43,
                        31,
                        10,
                        14,
                        59,
                        39,
                        21,
                        24,
                        37,
                        60,
                        50
                        ],axis=1)
    testx = testx.drop([0,
                          1,
                          49,
                          51,
                          9,
                          16,
                          62,
                          13,
                          11,
                          6,
                          17,
                          46,
                          7,
                          42,
                          34,
                          55,
                          61,
                          3,
                          18,
                          29,
                          53,
                          47,
                          27,
                          2,
                          44,
                          48,
                          35,
                          56,
                          52,
                          30,
                          19,
                          15,
                          32,
                          43,
                          31,
                          10,
                          14,
                          59,
                          39,
                          21,
                          24,
                          37,
                          60,
                          50
                          ], axis=1)
    model = GradientBoostingClassifier().fit(trainx, np.array(trainy).ravel())
    #model=DecisionTreeClassifier().fit(trainx, np.array(trainy).ravel())
    pre = model.predict(testx)
    C = confusion_matrix(testy, pre)
    print(C)
    #err = (np.mean((pre != np.array(testy).ravel())))
    #print(err)
    auc = roc_auc_score(testy, pre)
    print('AUC:', auc)