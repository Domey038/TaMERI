from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import pickle
import pandas as pd

def prepare_data(data_set):
    data_set = data_set.drop('car_name', axis=1)
    x = data_set.drop('mpg',axis=1)
    y = data_set['mpg']
    return x,y

def one_hot_encoder(data, cols):
    #One-hot encode categorical variables
    enc = OneHotEncoder(categorical_features=cols, handle_unknown='error', n_values='auto', sparse=True)
    data_OHE = enc.fit_transform(data).toarray()
    data_OHE_pd = pd.DataFrame(data_OHE)
    return data_OHE_pd

def split_data(x, y):
    #split data
    x_train, x_test, y_train, y_test = train_test_split(x, y)
    return x_train, x_test, y_train, y_test

def create_fitting(data):
    scaler = StandardScaler()
    scaler.fit(data)
    pickle.dump(scaler, open("data/scaling.pickle", 'wb'))

def fit_data(data):
    scaler = pickle.load(open("data/scaling.pickle", 'rb'))
    data_fitted = scaler.transform(data)
    return data_fitted
