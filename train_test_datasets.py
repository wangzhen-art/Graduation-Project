import pandas
import numpy as np
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split

data0 = pandas.read_csv("./pre_datasets/pre_UNSW-NB15_1.csv", header=None)
data1 = pandas.read_csv("./pre_datasets/pre_UNSW-NB15_2.csv", header=None)
data2 = pandas.read_csv("./pre_datasets/pre_UNSW-NB15_3.csv", header=None)
data3 = pandas.read_csv("./pre_datasets/pre_UNSW-NB15_4.csv", header=None)

data0=pandas.DataFrame(data0)
data1=pandas.DataFrame(data1)
data2=pandas.DataFrame(data2)
data3=pandas.DataFrame(data3)

data=pandas.concat([data0,data1,data2,data3])


    #去除nan
print(np.any(np.isnan(data)))
data=data.dropna(axis=0,how='any')
print(np.any(np.isnan(data)))

Y = data[0]
X = data.drop([0],axis=1)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

model=XGBClassifier(
    learning_rate=0.1,
    n_estimators=1,
    max_depth=5,
    min_child_weight=1,
    gamma=0,
    subsample=0.8,
    xolsample_bytree=0.8,
    scale_pos_weight=1,
    objective='multi:softmax',
    num_class=10,
    nthread=4,
    seed=27)

model.fit(X_train,Y_train)
model.feature_importances_
# plt.bar(range(len(model.feature_importances_)), model.feature_importances_)
# plt.savefig("./picture/xgb_importances.jpg") 
# plt.show()

model1 = SelectFromModel(model,threshold=0.0015,prefit=True)
X_train = model1.transform(X_train)
X_test = model1.transform(X_test)
print(X_train.shape) 
print(X_test.shape)

from imblearn.over_sampling import SMOTE
smo = SMOTE(ratio={1: 300 },random_state=42)

X_train = pandas.DataFrame(X_train)
X_test = pandas.DataFrame(X_test)

print('Save processed files')
X_train.to_csv("./train_test_datasets/X_train.csv",mode='a',index=False,header=None,sep=",")
X_test.to_csv("./train_test_datasets/X_test.csv",mode='a',index=False,header=None,sep=",")
Y_train.to_csv("./train_test_datasets/Y_train.csv",mode='a',index=False,header=None,sep=",")
Y_test.to_csv("./train_test_datasets/Y_test.csv",mode='a',index=False,header=None,sep=",")
