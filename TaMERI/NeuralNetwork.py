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
#          Functions of class neural_network          #
#-----------------------------------------------------#
class neural_network:
    #initialize class variables
    model = None

    #Create a neural network model with fixed parameters
    def __init__(self):
        self.model = MLPRegressor(hidden_layer_sizes=fixed_hidden_layer_sizes, max_iter=fixed_max_iters,
                                  solver=fixed_solver, activation=fixed_activation)

    #Train the neural network model according to provided training data set
    def train(self, train_x, train_y):
        self.model.fit(train_x, train_y)

    #Use the provided neural network model to make predictions with the provided data
    def predict(self, data):
        predictions = self.model.predict(data)
        return predictions

    #Save/dump a neural network model to disk for later usage
    def dump(self):
        with open("model/NN_model.pickle", 'wb') as nn_dump:
            pickle.dump(self.model, nn_dump, protocol=pickle.HIGHEST_PROTOCOL)

    #Load a neural network model from disk
    def load(self):
        with open("model/NN_model.pickle", 'rb') as nn_load:
            self.model = pickle.load(nn_load)

    # #PLACEHOLDER
    # def calibrate(x, y):
    #     from sklearn.model_selection import GridSearchCV
    #     model = MLPRegressor(max_iter=15000)
    #     param_grid = [{'activation':['identity', 'logistic', 'tanh', 'relu'],
    #                 'solver':['lbfgs', 'adam'],
    #                 'hidden_layer_sizes':[(1), (5), (10), (15), (20), (1,1), (5,5), (10,10), (15,15), (20,20), (10,5), (5,10)]}]
    #     clf = GridSearchCV(model, param_grid, cv=3, scoring='neg_mean_absolute_error')
    #     clf.fit(x,y)
    #
    #     print("Best parameters set found on development set:")
    #     print(str(best_score_) + "\t" + str(clf.best_params_))
    #     print(cv_results_)
