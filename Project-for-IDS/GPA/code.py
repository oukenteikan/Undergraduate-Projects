import pandas as pd
import numpy as np
from sklearn.linear_model import RidgeCV,ElasticNetCV,LassoLarsCV,SGDRegressor
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
p1="TrainData.xlsx"
p2 = "TestData.xlsx"
train = pd.read_excel(p1)
test = pd.read_excel(p2)
trainx = pd.read_csv("trainx.csv", encoding = 'gbk')
testx = pd.read_csv("testx.csv", encoding = 'gbk')
trainy = pd.read_csv("trainy.csv", encoding = "utf-8")
trainx11=pd.read_csv('trainx_new11.csv',encoding='gbk')
testx11=pd.read_csv('testx_new11.csv',encoding='gbk')
trainy = 100 - ((4.0 - trainy)/3*1600)**(0.5)
train = train.drop([u'进步情况', u'专利数', u'社会活动', u'获奖数', u'竞赛成绩', u'综合GPA',u'性别',u'民族',\
                    u'院系',u'外语语种',u'高三排名',u'政治面貌', u'裸眼视力(左)', u'裸眼视力(右)', u'色盲',\
                    u'身高', u'体重',u'考生类型',u'优惠加分', u'大类',u'学生ID',u'生源省市',u'科类',u'中学'],axis = 1)
test = test.drop([u'进步情况', u'专利数', u'社会活动', u'获奖数', u'竞赛成绩', u'性别',u'民族',\
                  u'院系',u'外语语种',u'高三排名',u'政治面貌', u'裸眼视力(左)', u'裸眼视力(右)', u'色盲',\
                  u'身高', u'体重',u'考生类型',u'优惠加分', u'大类',u'学生ID',u'生源省市',u'科类',u'中学'],axis = 1)
merge = pd.concat([train,test])
merge.columns.values[0] = u'年龄'
merge[u'年龄'] = merge[u'年份'] - merge[u'年龄']
merge[u'成绩方差'] = merge[u'成绩方差'].fillna(merge[u'成绩方差'].mean())

for i in range(4026):
    s1 = merge[u'成绩'][i]
    if np.isnan(s1):
        s2 = merge[u'投档成绩'][i]
        if not np.isnan(s2):
            merge.set_value(i, u'成绩', np.float64(int(s2)))
    else:
        s2 = merge[u'投档成绩'][i]
        if s2 - s1 > 1:
            merge.set_value(i, u'成绩', np.float64(int(s2)))
del merge[u'投档成绩']
zscore = lambda x : x / x.max()
transformed = group.transform(zscore)

temp=pd.DataFrame(columns=['中学','高三排名'])
temp['中学']=train_old['中学']
temp['高三排名']=train_old['高三排名']
temp1=pd.DataFrame(columns=['中学','高三排名'])
temp1['中学']=test_old['中学']
temp1['高三排名']=test_old['高三排名']
temp=temp.append(temp1,ignore_index=True)
temp['flag']=0

flag=0
for i in range(len(temp)):
    if(temp.loc[i,'flag']==1):
        continue
    sch=temp[temp['中学']==temp['中学'][i]]
    sch=sch[sch['高三排名']<1]
    lennotnull=len(sch[~sch['高三排名'].isnull()==True])
    if(lennotnull<=1):
        flag=1
        temp.loc[temp['中学'] == temp['中学'][i], 'flag'] = 1
        continue
    med=np.median(sch[~sch['高三排名'].isnull()]['高三排名'])
    if sch[~sch['高三排名'].isnull()]['高三排名'].shape[0]==1:
        rank = med
    else:
        rank=2*med   #考上北大相对人数越多，值越大
    train_new.loc[train_old['中学'] == temp['中学'][i],'中学' ] = rank
    test_new.loc[test_old['中学'] == temp['中学'][i], '中学'] = rank
    temp.loc[temp['中学'] == temp['中学'][i], 'flag'] = 1

mean=(len(train_new[~train_new['中学'].isnull()==True]['中学'])*np.mean(train_new[~train_new['中学'].isnull()==True]['中学'])+len(test_new[~test_new['中学'].isnull()==True]['中学'])*np.mean(test_new[~test_new['中学'].isnull()==True]['中学']))/(len(train_new[~train_new['中学'].isnull()==True]['中学'])+len(test_new[~test_new['中学'].isnull()==True]['中学']))
train_new.loc[train_new['中学'].isnull()==True, '中学'] = mean
test_new.loc[test_new['中学'].isnull()==True, '中学'] = mean

train_old=pd.read_csv('TrainData.csv',encoding='gbk')
test_old=pd.read_csv('TestData.csv',encoding='gbk')
train_new=pd.DataFrame(columns=['编号','中学'])
test_new=pd.DataFrame(columns=['编号','中学'])
train_new['编号']=train_old['编号']
test_new['编号']=test_old['编号']

temp=pd.DataFrame(columns=['中学','综合GPA'])
temp['中学']=train_old['中学']
temp['综合GPA']=train_old['综合GPA']
#temp=temp.append(temp1,ignore_index=True)
temp['flag']=0
for i in range(len(temp)):
    if(temp.loc[i,'flag']==1):
        continue
    sch=temp[temp['中学']==temp['中学'][i]]
    med=np.median(sch['综合GPA'])
    train_new.loc[train_old['中学'] == temp['中学'][i],'中学' ] = med
    test_new.loc[test_old['中学'] == temp['中学'][i], '中学'] = med
    temp.loc[temp['中学'] == temp['中学'][i], 'flag'] = 1

mean=(len(train_new[~train_new['中学'].isnull()==True]['中学'])*np.mean(train_new[~train_new['中学'].isnull()==True]['中学'])+len(test_new[~test_new['中学'].isnull()==True]['中学'])*np.mean(test_new[~test_new['中学'].isnull()==True]['中学']))/(len(train_new[~train_new['中学'].isnull()==True]['中学'])+len(test_new[~test_new['中学'].isnull()==True]['中学']))
train_new.loc[train_new['中学'].isnull()==True, '中学'] = mean
test_new.loc[test_new['中学'].isnull()==True, '中学'] = mean
train_new.to_csv('train_school.csv',encoding='gbk')
test_new.to_csv('test_school.csv',encoding='gbk')



train_new=train_new.drop(['编号'],axis=1)
test_new=test_new.drop(['编号'],axis=1)


trainx11['flag']=0
department={}
for i in range(3026):
    if trainx11.loc[i,'flag']==1:
        continue;
    mean=np.mean(trainy.loc[trainx11[u'院系']==trainx11.loc[i,u'院系'],u'综合GPA'])
    std=np.std(trainy.loc[trainx11[u'院系']==trainx11.loc[i,u'院系'],u'综合GPA'])
    department[trainx11.loc[i,u'院系']]=[mean,std]
    trainx11.loc[trainx11[u'院系']==trainx11.loc[i,u'院系'],'flag']=1
for i in range(3026):
    trainy.loc[i,u'综合GPA']=(trainy.loc[i,u'综合GPA']-department[trainx11.loc[i,u'院系']][0])/department[trainx11.loc[i,u'院系']][1]

data=pd.concat([trainx,testx])
data=data.drop(['纳西族','仡佬族','仫佬族','畲族','傣族','水族','日语','锡伯族','布朗族'],axis=1)
trainx=data.iloc[0:3026,:]
testx=data.iloc[3026:4026,:]

data=data.drop('优惠加分',axis=1)
data=pd.concat([data,score],axis=1)
data.loc[:,'优惠加分']=preprocessing.scale(data.loc[:,'优惠加分'])
trainx=data.iloc[0:3026,:]
testx=data.iloc[3026:4026,:]

trainx=trainx.drop('裸眼视力左',axis=1)
testx=testx.drop('裸眼视力左',axis=1)

sample = pd.read_csv("submission_sample.csv")
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import GradientBoostingRegressor
model = GradientBoostingRegressor(learning_rate=0.05,n_estimators=900,max_depth=2).fit(trainx,np.array(trainy).ravel())
testy = model.predict(testx)
for i in range(1000):
    testy[i]=testy[i]*department[testx11.loc[i,u'院系']][1]+department[testx11.loc[i,u'院系']][0]
sample["综合GPA"] = testy
sample["综合GPA"] = 4 - ((100 - sample["综合GPA"])**2)*3/1600
sample.to_csv("answer_1.csv", index = False)

sample = pd.read_csv("submission_sample.csv")
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=900).fit(trainx,np.array(trainy).ravel())
testy = model.predict(testx)
for i in range(1000):
    testy[i]=testy[i]*department[testx11.loc[i,u'院系']][1]+department[testx11.loc[i,u'院系']][0]
sample["综合GPA"] = testy
sample["综合GPA"] = 4 - ((100 - sample["综合GPA"])**2)*3/1600
sample.to_csv("answer_2.csv", index = False)

sample = pd.read_csv("submission_sample.csv")
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import GradientBoostingRegressor
model = GradientBoostingRegressor(learning_rate=0.05,n_estimators=900,max_depth=2).fit(trainx,np.array(trainy).ravel())
testy = model.predict(testx)
for i in range(1000):
    testy[i]=testy[i]*department[testx11.loc[i,u'院系']][1]+department[testx11.loc[i,u'院系']][0]
sample["综合GPA"] = testy
sample["综合GPA"] = 4 - ((100 - sample["综合GPA"])**2)*3/1600
sample.to_csv("answer_3.csv", index = False)



sample = pd.read_csv("submission_sample.csv")
from sklearn.linear_model import LassoLarsCV
model = LassoLarsCV(cv=30).fit(trainx,np.array(trainy).ravel())
testy = model.predict(testx)
for i in range(1000):
    testy[i]=testy[i]*department[testx11.loc[i,u'院系']][1]+department[testx11.loc[i,u'院系']][0]
sample["综合GPA"] = testy
sample["综合GPA"] = 4 - ((100 - sample["综合GPA"])**2)*3/1600
sample.to_csv("answer_4.csv", index = False)

sample = pd.read_csv("submission_sample.csv")
from sklearn.linear_model import SGDRegressor
model = SGDRegressor(alpha=0.001).fit(trainx,np.array(trainy).ravel())
testy = model.predict(testx)
for i in range(1000):
    testy[i]=testy[i]*department[testx11.loc[i,u'院系']][1]+department[testx11.loc[i,u'院系']][0]
sample["综合GPA"] = testy
sample["综合GPA"] = 4 - ((100 - sample["综合GPA"])**2)*3/1600
sample.to_csv("answer_5.csv", index = False)

sample = pd.read_csv("submission_sample.csv")
from sklearn.linear_model import ElasticNetCV
model = ElasticNetCV(cv=30).fit(trainx,np.array(trainy).ravel())
testy = model.predict(testx)
for i in range(1000):
    testy[i]=testy[i]*department[testx11.loc[i,u'院系']][1]+department[testx11.loc[i,u'院系']][0]
sample["综合GPA"] = testy
sample["综合GPA"] = 4 - ((100 - sample["综合GPA"])**2)*3/1600
sample.to_csv("answer_6.csv", index = False)
