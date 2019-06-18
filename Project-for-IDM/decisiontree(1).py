import pandas as pd
import numpy as np
import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix
from sklearn import svm
import sklearn.tree as tree
for y in range(5):
    data=pd.read_csv(str(y+1)+'year_withoutmiss.csv',header=None,na_values='?')
    data = data[(data[64] == 0) | (data[64] == 1)]
    data1 = data[data[64] == 1]
    data0=data[data[64]==0]
    #data0=data0.sample(n=data1.shape[0])
    data0=data0.loc[0:data1.shape[0], :]
    data=pd.concat([data1,data0])
    #data=data.drop([0,2,3,6,7,10,11,13,15,16,17,19,21,22,25,29,35,36,42,43,47,48,49,50,51,53,61],axis=1)
    trainx,testx,trainy,testy = train_test_split(data.iloc[:,0:64], data[64], test_size=0.25)
    trainy=pd.DataFrame(trainy)
    testy=pd.DataFrame(testy)
    #model=DecisionTreeClassifier(max_leaf_nodes=100).fit(trainx,trainy)
    #model = DecisionTreeClassifier().fit(trainx, trainy)
    model = GradientBoostingClassifier(n_estimators=1000).fit(trainx, np.array(trainy).ravel())
    #model = svm.SVC(class_weight='balanced').fit(trainx,np.array(trainy).ravel())
    pre=model.predict(testx)
    #imp=pd.DataFrame(model.feature_importances_)
    #imp.to_csv(str(y+1)+'importance.csv',index=False)
    C = confusion_matrix(testy, pre)
    print(C)
    err = (np.mean((pre != np.array(testy).ravel())))
    print(err)
    #tree.export_graphviz(model,out_file="tree.dot")
    import pydotplus
    from IPython.display import Image
    #dot_data = tree.export_graphviz(model, out_file=None,
    #filled=True, rounded=True,
    #special_characters=True)
    #graph = pydotplus.graph_from_dot_data(dot_data)
    #Image(graph.create_png())
    #graph.write_png("1-40.png")