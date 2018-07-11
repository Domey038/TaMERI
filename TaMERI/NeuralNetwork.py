#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
import Preprocessing as PC
import pickle
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error

#-----------------------------------------------------#
#           Fixed neural network parameters           #
#-----------------------------------------------------#
fixed_hidden_layer_sizes = (10)
fixed_max_iters = 15000
fixed_activation = 'relu'
fixed_solver = 'adam'

#-----------------------------------------------------#
#           -           #
#-----------------------------------------------------#
 
def create_NeuralNetwork():
    neural_network = MLPRegressor(hidden_layer_sizes=fixed_hidden_layer_sizes, max_iter=fixed_max_iters,
                                  solver=fixed_solver, activation=fixed_activation)
    return neural_network

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
    model = pickle.load(open("model/NN_model.pickle", 'rb'))
    predictions = model.predict(data)
    return predictions
