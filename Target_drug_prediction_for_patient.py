# -*- coding: utf-8 -*-
"""

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oVdYltWqDHvoR8xreP_zbZGnLMcAXhph
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

file=r"train.parquet"

test_file=r"test.parquet"

train_data=pd.read_parquet(file,engine='auto')#Reading the dataset

test_data=pd.read_parquet(test_file,engine='auto')

train_data.head()

test_data.head()

"""## EDA"""

print(train_data.shape,train_data.columns)
print()
print(test_data.shape,test_data.columns)

train_data.info()

test_data.info()

# Checking any duplicate records in train and test data
print(train_data.duplicated().sum())
print()
print(test_data.duplicated().sum())

#Checking for null values in both train and test data
print("Total NULL values in train data = ",train_data.isnull().sum().sum())
print()
print("Total NULL values in test data = ",test_data.isnull().sum().sum())

#Checking Unique values in each columns in both train and test
def info_col(train,feature):
    print("Unique valies in ", feature  ,len(train[feature].unique()))
    print()

for f in train_data[['Patient-Uid', 'Date', 'Incident']]:
    info_col(train_data,f)

#For testing data
def info_col(test,feature):
    print("Unique valies in ", feature  ,len(test[feature].unique()))
    print()

for f in test_data[['Patient-Uid', 'Date', 'Incident']]:
    info_col(test_data,f)

#checking total nuber of TARGET DRUG in Incident column in train data
len(train_data[train_data['Incident']=='TARGET DRUG'])

#checking total nuber of TARGET DRUG in Incident column in test data
len(test_data[test_data['Incident']=='TARGET DRUG'])

#Checking the top 10 total number of each categories in Incident
train_data['Incident'].value_counts().sort_values(ascending=False).head(10)

#visualization of most freaquent categories and their count in Incident columns
fig, ax = plt.subplots(figsize=(20,6))
sns.countplot(x=train_data.Incident.value_counts().sort_values(ascending=False).head(10), data=train_data)

"""## FEATURE ENGINEERING

"""

# Rmove all duplicates data from train and test data
train_data.drop_duplicates(inplace=True)

test_data.drop_duplicates(inplace=True)

print(train_data.duplicated().sum())
print()
print(test_data.duplicated().sum())

print(train_data.shape)
print()
print(test_data.shape)

"""### Pre-processing feature Patient-Uid

##### Datas in Patient-Uid in text format . So , here i am using NLP technique Bagofwords
"""

import nltk
import re
from nltk.corpus import stopwords

nltk.download('stopwords')

"""####### Reseting the index of both train and test data,Because index are not in correct order

"""

train_data.index[2]#So,there is no index of 2

train_data.reset_index(inplace=True)

train_data.drop('index',axis=1,inplace=True)

train_data.index[2]#Now its ok.

train_data.head(3)

test_data.index[5]

test_data.reset_index(inplace=True)

test_data.drop('index',axis=1,inplace=True)

test_data.head(6)



#spliting the data for pre-processing train data
PatientUid_list = []
for i in range(0, len(train_data)):
    PatientUid = train_data['Patient-Uid'][i].split('-')
    PatientUid = ' '.join(PatientUid)
    PatientUid_list.append(PatientUid)

#spliting the data for pre-processing test data
PatientUid_listtst = []
for i in range(0, len(test_data)):
    PatientUid = test_data['Patient-Uid'][i].split('-')
    PatientUid = ' '.join(PatientUid)
    PatientUid_listtst.append(PatientUid)

PatientUid_list[0:5]

PatientUid_listtst[0:5]

from tensorflow.keras.preprocessing.text import one_hot
voc_size=4000 # Considering total size of word

# applying one hot encoding on train and test data for coverting each word to neumeric values
onehot_PUID=[one_hot(words,voc_size)for words in PatientUid_list]
onehot_PUID

Patient_UIDdata=np.array(onehot_PUID)

Patient_UIDdata

Patient_UIDdata.shape

Patient_UIDdata=pd.DataFrame(Patient_UIDdata)

Patient_UIDdata.shape

Patient_UIDdata.head()

train_datacpy=train_data.copy()

train_datacpy.head()



finaltrain_data=pd.concat([train_datacpy, Patient_UIDdata], axis=1)

finaltrain_data.head()

finaltrain_data.dtypes

#Removing Patient-UID
finaltrain_data=finaltrain_data.drop('Patient-Uid',axis=1)

finaltrain_data

#for test data
onehot_PUIDtst=[one_hot(words,voc_size)for words in PatientUid_listtst]
onehot_PUIDtst

Patient_UIDdatatst=np.array(onehot_PUIDtst)

Patient_UIDdatatst

Patient_UIDdatatst.shape

Patient_UIDdatatstdf=pd.DataFrame(Patient_UIDdatatst)

Patient_UIDdatatstdf.head()

test_datacp=test_data.copy()

finaltest_data=pd.concat([test_datacp, Patient_UIDdatatstdf], axis=1)

#Removing Patient-UID
finaltest_data=finaltest_data.drop('Patient-Uid',axis=1)

finaltest_data.head()

"""### Pre-processing on Date column"""

finaltrain_data['Date'].dtypes

import datetime as dt

#finaltrain_data=finaltrain_data.drop('Month',axis=1)

finaltrain_data['Month']=finaltrain_data['Date'].dt.month
finaltrain_data['day']=finaltrain_data['Date'].dt.day
finaltrain_data['Year']=finaltrain_data['Date'].dt.year



finaltrain_data

"""### For test data"""

finaltest_data['Month']=finaltest_data['Date'].dt.month
finaltest_data['day']=finaltest_data['Date'].dt.day
finaltest_data['Year']=finaltest_data['Date'].dt.year

finaltest_data.head()





"""### Label Encodig"""

from sklearn import preprocessing

label_encoder = preprocessing.LabelEncoder()

finaltrain_data['Incidentlb']=label_encoder.fit_transform(finaltrain_data['Incident'])

finaltrain_data.head()

"""## on test data"""

finaltest_data['Incidentlbtst']=label_encoder.fit_transform(finaltest_data['Incident'])

finaltest_data.head()

"""## Creating new column for out Objective

Each patient-uid should be labeled with a binary value of 1 or 0 using the built
model, 1 is considered as eligible for the “Target Drug” in the next 30 days and 0
considered as un-eligible
"""

finaltrain_data['Target']=np.where(finaltrain_data['Incident']=='TARGET DRUG',1,0)

sns.countplot(finaltrain_data['Target'])

finaltrain_data=finaltrain_data.drop('Incident',axis=1)

finaltrain_data=finaltrain_data.drop('Date',axis=1)

finaltrain_data

len(finaltrain_data[finaltrain_data['Target']==1])

len(test_data[test_data['Incident']=='TARGET DRUG'])

#Removing Datae and Incident columns from test data

finaltest_data=finaltest_data.drop(['Date','Incident'],axis=1)

finaltest_data.head()

finaltest_data.shape

"""# Handling imbalanced data"""

finaltrain_data['Target'].value_counts()

sns.countplot(finaltrain_data['Target'])

"""Scaling the features is to avoid intensive computation and also avoid one variable dominating the others. For a binary classification problem, no need to scale the dependent variable. But for regression, we need to scale the dependent variables.

## Oversampling
"""

#Taking class count of 1 an 0

count_class_0, count_class_1 = finaltrain_data['Target'].value_counts()

# Divide by class
class_0 = finaltrain_data[finaltrain_data['Target'] == 0]
class_1 = finaltrain_data[finaltrain_data['Target'] == 1]

count_class_0, count_class_1

# Oversample 1-class and concat the DataFrames of both classes
class_1_over =class_1.sample(count_class_0, replace=True)
final_data = pd.concat([class_0, class_1_over], axis=0)

print('Random over-sampling:')
print(final_data.Target.value_counts())

#Final data for model
final_data.head()

sns.countplot(final_data['Target'])

"""# Feature Selection

In this case  , not do any kind of features of selection because  here we having only very less number of features, all of these features are important for the model training.

# Model Creation
"""

final_datacop=final_data.copy

#split the traimn data into input and output
x=final_data.drop('Target',axis=1)
y=final_data['Target']

x.head()

y.head()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=42)

print(X_train.shape,'\n')
print(X_test.shape,'\n')
print(y_train.shape,'\n')
print(y_test.shape)

print(y_test.value_counts())
print()
print(y_train.value_counts())



import tensorflow
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

from sklearn.metrics import roc_auc_score, f1_score

y_train.value_counts()

len(X_train.columns)

input_=9

"""## Creating Neural Network"""

model = Sequential()
# define first hidden layer and visible layer
model.add(Dense(50, input_dim=input_, activation='relu', kernel_initializer='he_uniform'))
# define output layer
model.add(Dense(1, activation='sigmoid'))
# define loss and optimizer
model.compile(loss='binary_crossentropy', optimizer='adam')
model.fit(X_train,y_train,epochs=10)

y_pred1=model.predict(X_test)

y_pred1

y_pred1lst=[]
for val in y_pred1:

    if val>0.5:
        val=1
    else:
        val=0
    y_pred1lst.append(val)


    #print(i)

y_pred1lst

yp=pd.DataFrame(y_pred1lst)

roc_auc_score(y_test,y_pred1lst)

from sklearn.metrics import classification_report

from sklearn.metrics import f1_score

f1_score(y_test, y_pred1lst, average='macro')

"""# Standardization"""

final_data

Xinp=final_data.drop('Target',axis=1)
Yinp=final_data['Target']

Xinp

Yinp

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

Xinpcpy=Xinp.copy



std_data=scaler.fit_transform(Xinp)

std_data

final_X=pd.DataFrame(std_data,columns=Xinp.columns)

final_X

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(final_X, y, test_size=0.30, random_state=42)



model.fit(X_train,y_train,epochs=10)

std_pred=model.predict(X_test)

roc_auc_score(y_test,std_pred)

std_pred

std_predlst=[]
for i in std_pred:
    if i >0.5:
        i=1
    else:
        i=0
    std_predlst.append(i)

std_predlst

"""# After standardization ,model will shows better accuraccy"""

f1_score(y_test,std_predlst, average='macro')

"""## applying standard scaler on test data"""

std_tstdata=scaler.fit_transform(finaltest_data)

std_tstdata

final_tst=pd.DataFrame(std_tstdata,columns=finaltest_data.columns)

final_tst

test_pred=model.predict(final_tst)

test_pred

std_predtst=[]
for i in test_pred:
    if i >0.5:
        i=1
    else:
        i=0
    std_predtst.append(i)

std_predtst

final_sub=pd.DataFrame(std_predtst,columns=['label'])

final_sub

final_sub=pd.concat([test_data,final_sub],axis=1)

final_sub

final_sub=final_sub.drop(['Date','Incident'],axis=1)

final_sub.duplicated().sum()

final_sub=final_sub.drop_duplicates()

final_sub.duplicated().sum()

final_sub

final_submission=pd.read_csv('final_submission.csv')

final_submission

