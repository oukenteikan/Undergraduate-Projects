import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LassoLarsCV
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
fan=pd.read_csv('concatnew/concatnew5.csv')
fan=fan.drop(range(7762,8722),axis=0)
#
# #T平滑
# day=[range(3,31),range(1,32),range(1,31),range(1,10)]
# temp=fan.loc[(fan['month']==4) & (fan['day']==3),'P'].reset_index(drop=True)
# for m in range(4):
#     for d in day[m]:
#         if (d==2) & (d==10):
#             continue
#         temp=pd.concat([temp,fan.loc[(fan['month']==m+4) & (fan['day']==d),'P'].reset_index(drop=True)],axis=1,ignore_index=True)
# temp_mean=temp.mean(axis=1)
#
# temp_mean=pd.concat([fan.loc[(fan['month']==4) & (fan['day']==3),'time'].reset_index(drop=True),temp_mean],axis=1)
# #
# for i in range(fan.shape[0]):
#     fan.loc[i,'P']=fan.loc[i,'P']-float(temp_mean[temp_mean['time']==fan.loc[i,'time']][0])

fan=fan.drop(['u','v','w','T','ppntspeed'],axis=1)

train=fan[fan['month']<7]
train_temp1=fan[(fan['month']==7) & (fan['day']<=8)]
train_temp2=fan[(fan['month']==7) & (fan['day']==9) & (fan['time']<=43200)]
train=pd.concat([train,train_temp1,train_temp2],axis=0)
pred=pd.DataFrame()
pred1=pd.DataFrame()
pred2=pd.DataFrame()
testy=pd.DataFrame()
for d in range(11,31):
    train_temp1 = fan[(fan['month'] == 7) & (fan['day'] == d-2)& (fan['time'] > 43200)]
    train_temp2 = fan[(fan['month'] == 7) & (fan['day'] == d-1) & (fan['time'] <= 43200)]
    train = pd.concat([train, train_temp1, train_temp2], axis=0)
    trainy=train['speed']
    trainx=train.drop(['speed'],axis=1)
    test=fan[(fan['month'] == 7) & (fan['day'] == d)]
    testx=test.drop(['speed'],axis=1)
    data=pd.concat([trainx,testx],ignore_index=True)
    data.drop(['month','day'],axis=1)
    #data['month'] = data['month'].astype('str')
    #data['day'] = data['day'].astype('str')
    data['time'] = data['time'].astype('str')
    data = pd.get_dummies(data,drop_first=True)
    trainx=data.loc[0:trainx.shape[0]-1,:]
    testx = data.loc[trainx.shape[0]:data.shape[0], :]
    #testx=testx.drop(['day','month'],axis=1)
    #trainx = trainx.drop(['day','month'], axis=1)

    #svr_rbf=SVR(kernel='rbf').fit(trainx,trainy)
    #pred_temp=svr_rbf.predict(testx)

    #svr_sigmoid=SVR(kernel='sigmoid').fit(trainx,trainy)
    #pred_temp=svr_sigmoid.predict(testx)

    #svr_linear=SVR(kernel='linear').fit(trainx,trainy)
    #pred_temp=svr_linear.predict(testx)

    #svr_poly=SVR(kernel='poly').fit(trainx,trainy)
    #pred_temp=svr_poly.predict(testx)

    #svr_precomputed=SVR(kernel='precomputed').fit(trainx,trainy)
    #pred_temp=svr_precomputed.predict(testx)

    #DBR=GradientBoostingRegressor().fit(trainx,trainy)
    #pred_temp=DBR.predict(testx)

    #DBR=GradientBoostingRegressor(n_estimators=500).fit(trainx,trainy)
    #pred_temp=DBR.predict(testx)

    #ridge = RidgeCV(cv=10).fit(trainx, trainy)
    #pred_temp = ridge.predict(testx)

    lassolars = LassoLarsCV(cv=10).fit(trainx, trainy)
    pred_temp = lassolars.predict(testx)


    #MLP=MLPRegressor(max_iter=500).fit(trainx,trainy)
    #pred_temp=MLP.predict(testx)
    #pred_train=ridge.predict(trainx)
    #magic=np.mean(trainy-pred_train)
    #print(magic)
    #pred_temp=pred_temp+magic
    #pred_temp=0.5*pred_temp1+0.5*pred_temp2
    #pred1=pd.concat([pred1,pd.DataFrame(pred_temp1)],axis=0)
    #pred2 = pd.concat([pred2, pd.DataFrame(pred_temp2)], axis=0)
    # pred_train=ridge.predict(trainx)
    # magic=np.mean(trainy-pred_train)
    # print(magic)
    # pred_temp=pred_temp+magic
    pred = pd.concat([pred, pd.DataFrame(pred_temp)], axis=0)
    testy=pd.concat([testy,test['speed']],axis=0)
    rmse = np.sqrt(mean_squared_error(pred_temp, test['speed']))/31.99531604
    print(d)
    print(rmse)
rmse=np.sqrt(mean_squared_error(pred,testy))/31.99531604
print(rmse)
#pred1=pred.copy()
#pred1.loc[pred[0]>np.mean(np.array(pred)),0]=(pred1.loc[pred[0]>np.mean(np.array(pred)),0]-np.mean(np.array(pred)))*3+np.mean(np.array(pred))
#pred1.loc[pred[0]<np.mean(np.array(pred)),0]=(pred1.loc[pred[0]<np.mean(np.array(pred)),0]-np.mean(np.array(pred)))*3+np.mean(np.array(pred))
#rmse=mean_squared_error(pred1,testy)
#print(rmse)




import matplotlib.pyplot as plt
plt.figure(figsize = (15, 10))
line1=plt.plot(range(1920), testy, 'b',label='testy')
line2=plt.plot(range(1920), pred,'g',label='LassoLars')
plt.legend(loc='upper left')
plt.show()
plt.savefig("1-LassoLars.png")
"""
import matplotlib.pyplot as plt
plt.figure(figsize = (15, 10))
ax1 = plt.subplot(211) # 在图表2中创建子图1
ax2 = plt.subplot(212) # 在图表2中创建子图2
plt.sca(ax1)  # ❷ # 选择图表2的子图1
plt.plot(range(96*5), fan.loc[(fan['month']==7) & (fan['day']>10) & (fan['day']<16),'T'], 'b')
plt.sca(ax2)  # 选择图表2的子图2
plt.plot(range(96*5), fan.loc[(fan['month']==7) & (fan['day']>10) & (fan['day']<16),'speed'],'g')
plt.show()
"""
#plt.plot(range(fan.shape[0]), fan['T'],'g')
#plt.show()

"""3.09
ridge = RidgeCV(cv=10).fit(trainx, trainy)
pred_temp2 = ridge.predict(testx)

MLP = MLPRegressor().fit(trainx, trainy)
pred_temp1 = MLP.predict(testx)
# pred_train=ridge.predict(trainx)
# magic=np.mean(trainy-pred_train)
# print(magic)
# pred_temp=pred_temp+magic
pred_temp = 0.1 * pred_temp1 + 0.9 * pred_temp2
"""