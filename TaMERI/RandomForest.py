#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
import Preprocessing as PC
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV

#-----------------------------------------------------#
#            Fixed random forest parameters           #
#-----------------------------------------------------#

#-----------------------------------------------------#
#          Functions of class random_forest           #
#-----------------------------------------------------#
class random_forest:
    #initialize class variables
    model = None

    #Create a random forest model with fixed parameters
    def __init__(self):
        self.model = RandomForestRegressor()

    #Train the random forest model according to provided training data set
    def train(self, train_x, train_y):
        self.model.fit(train_x, train_y)

    #Use the provided random forest model to make predictions with the provided data
    def predict(self, data):
        predictions = self.model.predict(data)
        return predictions

    #Save/dump a random forest model to disk for later usage
    def dump(self):
        with open("model/RF_model.pickle", 'wb') as rf_dump:
            pickle.dump(self.model, rf_dump, protocol=pickle.HIGHEST_PROTOCOL)

    #Load a random forest model from disk
    def load(self):
        with open("model/RF_model.pickle", 'rb') as rf_load:
            self.model = pickle.load(rf_load)

    #Automatically identify best parameters for the random forest model
    # def calibrate(self, x, y):
    #     self.model = MLPRegressor(max_iter=15000)
    #     param_grid = [{'activation':['identity', 'logistic', 'tanh', 'relu'],
    #                 'solver':['lbfgs', 'adam', 'sgd'],
    #                 'hidden_layer_sizes':[(1), (2), (3), (4), (5), (6), (7), (8), (9), (10),
    #                 (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10),
    #                 (15), (20), (15,15), (20,20), (10,5), (5,10), (3,5), (5,3)]}]
    #     clf = GridSearchCV(self.model, param_grid, cv=5, scoring='neg_mean_absolute_error')
    #     clf.fit(x,y)
    #     self.dump()
    #
    #     print("Best parameters set found on development set:")
    #     print(str(clf.best_score_) + "\t" + str(clf.best_params_))
    #     print(str(clf.cv_results_))
