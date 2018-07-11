from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
import Preprocessing as PC
import pickle

def calibrate_model_parameter(x, y):
    from sklearn.model_selection import GridSearchCV
    model = MLPRegressor(max_iter=15000)
    param_grid = [{'activation':['identity', 'logistic', 'tanh', 'relu'],
                'solver':['lbfgs', 'adam'],
                'hidden_layer_sizes':[(1), (5), (10), (15), (20), (1,1), (5,5), (10,10), (15,15), (20,20), (10,5), (5,10)]}]
    clf = GridSearchCV(model, param_grid, cv=3, scoring='neg_mean_absolute_error')
    clf.fit(x,y)

    print("Best parameters set found on development set:")
    print(str(best_score_) + "\t" + str(clf.best_params_))
    print(cv_results_)

def train_model(x, y):
    min_MAE = 1000000000000000
    best_hl = None
    best_model = None
    for i in range(1,20):
        MAE, model = training_iteration(x, y, (i), 5000)
        if MAE < min_MAE:
            min_MAE = MAE
            best_model = MAE
            best_hl = i
        print(str(i) + "\t" + str(MAE))
    print("Single-layer best model: " + str(best_hl) + "\t" + str(min_MAE))

    min_MAE = 1000000000000000
    best_hl = None
    best_model = None
    for i in range(1,20):
        for j in range(1,20):
            MAE, model = training_iteration(x, y, (i,j), 5000)
            if MAE < min_MAE:
                min_MAE = MAE
                best_model = MAE
                best_hl = (i,j)
            print(str(best_hl) + "\t" + str(MAE))
    print("BI-layer best model: " + str(best_hl) + "\t" + str(min_MAE))

def training_iteration(x, y, hls, iters):
    #preprocessing (splitting and fitting)
    x_train, x_test, y_train, y_test = PC.split_data(x,y)
    PC.create_fitting(x_train)
    x_train = PC.fit_data(x_train)
    x_test = PC.fit_data(x_test)
    #create the neural network
    model = MLPRegressor(hidden_layer_sizes=hls, max_iter=iters)
    model.fit(x_train, y_train)
    #test model
    pred = model.predict(x_test)
    #evaluate result
    MAE = mean_absolute_error(pred, y_test)
    #return results
    return MAE, model

def predict(data):
    model = pickle.load(open("data/NN_model.pickle", 'rb'))
    predictions = model.predict(data)
    return predictions
