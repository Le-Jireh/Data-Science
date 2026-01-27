import pandas as pd
import numpy as np
import matplotlib as plot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
import pickle

dataset=pd.read_csv("Bengaluru_House_Data.csv")
#print(dataset.groupby("area_type")["area_type"].agg("count"))
dataset=dataset.drop(["area_type", "society", "balcony", "availability"], axis=1)
#usualli if u have a small dataset u fill in the null values with the median. dataset.isnull().sum()
dataset=dataset.dropna()
dataset["rooms"]=dataset["size"].apply(lambda item: int(item.split(" ")[0]))

"""
def is_float(x):
    try:
        float(x)
    except:
        return False
    return True
#print(dataset[~dataset["total_sqft"].apply(is_float)])
"""

#this does account for different measurements
def convert_num(x):
    tokens=x.split("-")
    if len(tokens)==2:
        return (float(tokens[0])+float(tokens[1]))/2
    try:
        return float(x)
    except:
        return None
dataset["total_sqft"]=dataset["total_sqft"].apply(convert_num)
dataset=dataset[dataset.total_sqft.notnull()]
dataset["price_per_sqft"]=dataset["price"]*100000/dataset["total_sqft"]
locationStats=dataset.groupby("location")["location"].agg("count")
locLess10=locationStats[locationStats<=10]
dataset["location"]=dataset["location"].apply(lambda item: "other" if item in locLess10 else item)
#print(len(dataset.location.unique()))
dataset=dataset[~(dataset.total_sqft/dataset.rooms<300)]

def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df = subdf[(subdf.price_per_sqft>(m-st)) & (subdf.price_per_sqft<=(m+st))]
        df_out = pd.concat([df_out,reduced_df],ignore_index=True)
    return df_out
dataset=remove_pps_outliers(dataset)

def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('rooms'):
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }
        for bhk, bhk_df in location_df.groupby('rooms'):
            stats = bhk_stats.get(bhk-1)
            if stats and stats['count']>5:
                exclude_indices = np.append(exclude_indices, bhk_df[bhk_df.price_per_sqft<(stats['mean'])].index.values)
    return df.drop(exclude_indices,axis='index')
dataset = remove_bhk_outliers(dataset)

dummies= pd.get_dummies(dataset.location)
dataset = pd.concat([dataset, dummies.drop("other", axis=1)], axis=1)
dataset = dataset.drop(["location", "size", "price_per_sqft"], axis=1)
dependentDF=dataset.drop("price", axis=1)
indepDF=dataset.price
depTrain, depTest, indTrain, indTest=train_test_split(dependentDF, indepDF, test_size=.2, random_state=10)
lr_clf=LinearRegression()
lr_clf.fit(depTrain.values, indTrain)

#cv=ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)

#lasso, linear, regressionDecisionTree test which model is more fitting
def predict_price(location,sqft,bath,bhk):

    loc_index = np.where(dependentDF.columns==location)[0][0]
    x = np.zeros(len(dependentDF.columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    return lr_clf.predict([x])[0]

print(predict_price('1st Phase JP Nagar',1000, 3, 3))

with open("RegressionLogic.pickle", "wb") as f:
    pickle.dump(lr_clf, f)

import json
columns = {
    'data_columns' : [col.lower() for col in dependentDF.columns]}
with open("columns.json","w") as f:
    f.write(json.dumps(columns))
