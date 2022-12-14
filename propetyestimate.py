# -*- coding: utf-8 -*-
"""PropetyEstimate.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ctb2sr0ITN1sg4gner9_fQ7LE6QPMLg5
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from importlib import reload
import pickle
import json

from google.colab import files
uploaded=files.upload()

data=pd.read_csv('Bengaluru_House_Data.csv')

data.head()

data=data.drop(['area_type','availability','society'],axis=1)

data

data['size']=data['size'].str.split(' ',expand=True)[0].astype(float)

data.isnull().sum()

data=data.dropna()

data.dtypes

def convert(x):
  tokens=x.split('-')
  if len(tokens)==2:
    avg=(float(tokens[0])+float(tokens[1]))/2
    return avg
  else:
    try:
        return float(x)
    except:
        return None

data['total_sqft']=data['total_sqft'].apply(convert)

data.head(20)

data['size']=data['size'].astype(float)

data['size'].unique()

data['bath'].unique()

data['balcony'].unique()

data[data.bath>5].shape

data[data.bath>5]

data['sqft_per_bhk']=data['total_sqft']/data['size']

data['sqft_per_bhk']=data['sqft_per_bhk'].apply(lambda x: x if x>=250 else(None))

data=data.dropna()

data['price_per_sqft']=(data['price']/data['total_sqft'])*100000

data[data.price_per_sqft<1500]

data[data.price_per_sqft>10000]

def convert_price(x):
  if x>=1500 and x<=10000:
    return x
  else:
    return None

data['price_per_sqft']=data['price_per_sqft'].apply(convert_price)

data.shape

data.head(20)

data['location'].unique()

len(data['location'].unique())

data.groupby('location')['size'].count().unique()

data.groupby('location').get_group('Other').shape[0]

data

data['location']=data['location'].apply(lambda x: x if data.groupby('location').get_group(x).shape[0] >10 else('Other'))

data.describe()

data3.to_excel("Bengaluru_House_Data_updated.xlsx")
files.download("Bengaluru_House_Data_updated.xlsx")

from google.colab import files
uploaded=files.upload()

data=pd.read_csv('Bengaluru_House_Data_updated.csv')

data

def reduce_data(df):
  final_df=pd.DataFrame()
  for i,grp in df.groupby('location'):
    m=np.mean(grp.price_per_sqft)
    s=np.std(grp.price_per_sqft)
    reduced_df=grp[(grp.price_per_sqft >= m-s) & (grp.price_per_sqft <= m+s)]
    final_df=pd.concat([final_df,reduced_df],ignore_index=True)
  return final_df

def reduce_data2(df):
  final_df=pd.DataFrame()
  for i,grp in df.groupby('location'):
    m=np.mean(grp.sqft_per_bhk)
    s=np.std(grp.sqft_per_bhk)
    reduced_df=grp[(grp.sqft_per_bhk >= m-s) & (grp.sqft_per_bhk <= m+s)]
    final_df=pd.concat([final_df,reduced_df],ignore_index=True)
  return final_df

data1=reduce_data(data)

data1

data2=reduce_data2(data1)

data2.head(20)

data2.shape

data.shape

data1.shape

data2.shape

data2['size']=data2['size'].astype(int)

data2['bhk']=data2['size']

plt=reload(plt)

def plot_scatter_chart(df,location):
  grp=df.groupby('location').get_group(location)
  plt.rcParams['figure.figsize']=(15,10)
  df1=grp[(grp.location==location) & (grp.bhk==2)]
  df2=grp[(grp.location==location) & (grp.bhk==3)]
  plt.scatter(df1.total_sqft,df1.price,color='blue',label='2 BHK',s=50)
  plt.scatter(df2.total_sqft,df2.price,color='green',marker='+',label='3 BHK',s=50)
  plt.xlabel('Total Square feet',fontsize=10)
  plt.ylabel('Price',fontsize=10)
  plt.title(location)
  plt.legend()

plot_scatter_chart(data3,'Hebbal')

data2.groupby('location')['size'].count().head(50)

data2.bhk.unique()

data2=data2[data2.bhk<5]

def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('bhk'):
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }
        for bhk, bhk_df in location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk-1)
            if stats and stats['count']>5:
                exclude_indices = np.append(exclude_indices, bhk_df[bhk_df.price_per_sqft<(stats['mean'])].index.values)
    return df.drop(exclude_indices,axis='index')
data3 = remove_bhk_outliers(data2)
# df8 = df7.copy()
data3.shape

from google.colab import files
uploaded=files.upload()

data3=pd.read_excel('Bengaluru_House_Data_updated.xlsx')

data3

data3=data3.drop(['Unnamed: 0'],axis=1)

data3=data3[data3.bath <= data3.bhk]

plt=reload(plt)

plt.rcParams['figure.figsize']=(15,10)
plt.hist(data3.price_per_sqft,rwidth=.8)
plt.xlabel('Price per Squarefeet', fontsize=10)
plt.ylabel('Count', fontsize=10)

plt.rcParams['figure.figsize']=(15,10)
plt.hist(data3.sqft_per_bhk,rwidth=.8)
plt.xlabel('Squarefeet per bhk', fontsize=10)
plt.ylabel('Count', fontsize=10)

plt.rcParams['figure.figsize']=(15,10)
plt.hist(data3.balcony,rwidth=.8)
plt.xlabel('Balcony', fontsize=10)
plt.ylabel('Count', fontsize=10)

plt.rcParams['figure.figsize']=(15,10)
plt.hist(data3.bath,rwidth=.8)
plt.xlabel('Bathroom', fontsize=10)
plt.ylabel('Count', fontsize=10)

plt.rcParams['figure.figsize']=(15,10)
plt.hist(data3.bhk,rwidth=.8)
plt.xlabel('BHK', fontsize=10)
plt.ylabel('Count', fontsize=10)

data3

data3=data3.drop(['size','sqft_per_bhk','price_per_sqft'],axis=1)

data3

data3.to_excel("Bengaluru_House_Data_Modelready.xlsx")
files.download("Bengaluru_House_Data_Modelready.xlsx")

from google.colab import files
uploaded=files.upload()

data4=pd.read_excel("Bengaluru_House_Data_Modelready.xlsx")

data4=data4.drop(["Unnamed: 0"],axis=1)

data4

dummy=pd.get_dummies(data4.location)

data5=pd.concat([data4,dummy],axis=1)

data5

data5=data5.drop(['location'],axis=1)

data5

data5.to_csv("Model_Ready_data_Bengaluru.csv")

files.download("Model_Ready_data_Bengaluru.csv")

from google.colab import files
files.upload()

data5=pd.read_csv("Model_Ready_data_Bengaluru.csv")

data5

data5=data5.drop(["Unnamed: 0"],axis=1)

data5

def plot_scatter_chart(df,location):
  grp=df.groupby('location').get_group(location)
  plt.rcParams['figure.figsize']=(15,10)
  df1=grp[(grp.location==location) & (grp.bhk==2)]
  plt.scatter(df1.total_sqft,df1.price,color='blue',label='2 BHK',s=50)
  plt.xlabel('Total Square feet',fontsize=10)
  plt.ylabel('Price',fontsize=10)
  plt.title(location)
  plt.legend()

data5.groupby("location")['bhk'].count()

X=data5.drop(["price"],axis=1)
Y=data5["price"]

X

Y=pd.DataFrame(Y)

Y

from sklearn.model_selection import train_test_split, ShuffleSplit, cross_val_score, GridSearchCV

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=.2,random_state=10)

X_train

Y_train

from sklearn.linear_model import LinearRegression
reg=LinearRegression()
reg.fit(X_train , Y_train)
reg.score(X_test, Y_test)

cv=ShuffleSplit(n_splits=5,test_size=.3,random_state=10)
cross_val_score(LinearRegression(),X,Y,cv=cv)

from sklearn.linear_model import Lasso
lasso=Lasso()
lasso.fit(X_train , Y_train)
lasso.score(X_test, Y_test)

cross_val_score(Lasso(),X,Y,cv=cv)

from sklearn.linear_model import Ridge
Rid=Ridge()
Rid.fit(X_train , Y_train)
Rid.score(X_test, Y_test)

cross_val_score(Ridge(),X,Y,cv=cv)

gs=GridSearchCV(LinearRegression(),{'normalize':[True,False]},cv=cv, return_train_score=False)
gs.fit(X,Y)
gs.best_params_

gs.best_score_

gs=GridSearchCV(Lasso(),{'alpha':[1,2],'selection':['random','cylic']},cv=cv, return_train_score=False)
gs.fit(X,Y)
gs.best_params_

gs.best_score_

gs=GridSearchCV(Ridge(),{'alpha':[1,2],'normalize':[True,False]},cv=cv, return_train_score=False)
gs.fit(X,Y)
gs.best_params_

gs.best_score_

rid=Ridge(alpha=1,normalize=False)
rid.fit(X_train,Y_train)

import pickle
with open("model.pkl","wb") as f:
  pickle.dump(rid,f)

files.download("model.pkl")

columns={'columns':[col for col in X.columns]}

columns

import json
with open("Columns.json","w") as f:
  f.write(json.dumps(columns))

files.download("Columns.json")

with open("Columns.json","r") as f:
  col=json.load(f)["columns"]

col

def predict_price(sqft,bhk,bath,balcony,location):
  input=np.zeros(len(col))
  try:
    loc_index=col.index(location)
  except:
    loc_index=-1
  finally:
    input[0]=sqft
    input[1]=bath
    input[2]=balcony
    input[3]=bhk
    if loc_index>=0:
      input[loc_index]=1
  return rid.predict([input])[0][0]

predict_price(1000,2,2,1,'HBR Layout')