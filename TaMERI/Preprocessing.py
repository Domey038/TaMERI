#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder


#-----------------------------------------------------#
#               Preprocessing functions               #
#-----------------------------------------------------#
#Split a data set into data and results according to a provided colname
def split_data_from_results(data_set, colname):
    x = data_set.drop(colname, axis=1)
    y = data_set[colname]
    return x,y

#Remove non-finite values
def clean_data(data_set):
    data_set = data_set[np.isfinite(data_set['ER_ratio'])]
    return data_set

#Create dummy variables for the categorical variables to pseudo-continous variables
def create_dummy_variables(data_set, cols):
    for col in cols:
        dv = data_set[col].str.join('|').str.get_dummies()
        data_set = data_set.drop(col, axis=1)
        data_set = pd.concat([data_set, dv], axis=1)
    return data_set

#One-hot-encode (OHE) categorical variables to pseudo-continous variables
def one_hot_encoder(data, cols):
    enc = OneHotEncoder(categorical_features=cols, handle_unknown='error', n_values='auto', sparse=True)
    data_OHE = enc.fit_transform(data).toarray()
    data_OHE_pd = pd.DataFrame(data_OHE)
    return data_OHE_pd

#Create a standard scaling fitting of the data
def create_fitting(data):
    scaler = StandardScaler()
    scaler.fit(data)
    pickle.dump(scaler, open("model/scaling.pickle", 'wb'))

#Fitting of the data according to a already created standard scaling
def fit_data(data):
    scaler = pickle.load(open("model/scaling.pickle", 'rb'))
    data_fitted = scaler.transform(data)
    data_fitted = pd.DataFrame(data_fitted)
    return data_fitted
