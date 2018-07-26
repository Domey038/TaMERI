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
fixed_n_estimators = 5000
fixed_max_depth = None
fixed_max_features = 'sqrt'
fixed_min_samples_split = 2
fixed_min_samples_leaf = 9
fixed_bootstrap = True

#-----------------------------------------------------#
#          Functions of class random_forest           #
#-----------------------------------------------------#
class random_forest:
    #initialize class variables
    model = None

    #Create a random forest model with fixed parameters
    def __init__(self):
        self.model = RandomForestRegressor(random_state=0, n_estimators=fixed_n_estimators, max_depth=fixed_max_depth,
                                            min_samples_split=fixed_min_samples_split, min_samples_leaf=fixed_min_samples_leaf,
                                            bootstrap=fixed_bootstrap)

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
    def calibrate(self, x, y):
        self.model = RandomForestRegressor(random_state=0)
        param_grid = {"n_estimators": [50, 100, 150, 200, 500, 1000, 2500, 5000],
            "max_depth": [3, None],
            "max_features": ['auto', 'sqrt', 1, 3, 5, 10],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 3, 5, 7, 8, 9, 10],
            "bootstrap": [True, False]}
        clf = GridSearchCV(self.model, param_grid, cv=5, scoring='r2', n_jobs=-1)
        clf.fit(x,y)
        self.dump()

        print("Best parameters set found on development set:")
        print(str(clf.best_score_) + "\t" + str(clf.best_params_))
        print(str(clf.cv_results_))
