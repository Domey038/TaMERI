#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
#External libraries
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import explained_variance_score
#TaMERI libraries/scripts
import NeuralNetwork as TaMERI_NN

#-----------------------------------------------------#
#                 Validation functions                #
#-----------------------------------------------------#
#Perform a cross-validation for the neural network and calculate evaluation measurements
def cross_validation(set_x, set_y):
    #create a 5-fold cross-validation of the data set
    cross_val_folds = KFold(n_splits=5)
    folded_indices = cross_val_folds.split(set_x)

    #Iterate through each fold of the cross-validation
    current_fold = 1
    for train, test in folded_indices:
        #initialize the training and testing data sets according to fold indices
        train_x, test_x = set_x.iloc[train], set_x.iloc[test]
        train_y, test_y = set_y.iloc[train], set_y.iloc[test]

        #create an neural_network object
        neural_network = TaMERI_NN.neural_network()
        #train the neural network
        neural_network.train(train_x, train_y)
        #calculate predictions with the trained neural network model
        predictions = neural_network.predict(test_x)
        #calculate evaluation measurements of the predictions
        MAE, EVS = evaluate_predictions(predictions, test_y)
        #output the results of the current fold
        print("Fold " + str(current_fold) + " - " + "MAE: " + str(MAE))
        print("Fold " + str(current_fold) + " - " + "EVS: " + str(EVS))
        #dump the predictions<->real of the current fold
        dump_fold(predictions, test_y, current_fold)
        current_fold += 1

#Evaluate the predictions by comparing to the real values
def evaluate_predictions(pred, real):
    MAE = mean_absolute_error(real, pred)
    EVS = explained_variance_score(real, pred)
    return MAE,EVS

#Dump the results of the current fold in a file
def dump_fold(pred, real, fold_index):
    with open("data/cv.fold_" + str(fold_index) + ".tsv", 'w') as fold_dumper:
        fold_dumper.write("real" + "\t" + "pred" + "\n")
        real = real.tolist()
        for i, p in enumerate(pred):
            fold_dumper.write(str(real[i]) + "\t" + str(p) + "\n")
