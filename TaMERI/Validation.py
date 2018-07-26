#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
#External libraries
import os
import subprocess
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import r2_score
#TaMERI libraries/scripts
import NeuralNetwork as TaMERI_NN
import RandomForest as TaMERI_RF

#-----------------------------------------------------#
#                 Validation functions                #
#-----------------------------------------------------#
#Perform a cross-validation for the neural network and calculate evaluation measurements
def cross_validation(set_x, set_y, validation_ML_algorithm):
    #create a 5-fold cross-validation of the data set
    cross_val_folds = KFold(n_splits=5)
    folded_indices = cross_val_folds.split(set_x)

    #Iterate through each fold of the cross-validation
    current_fold = 1
    outcome_data = []
    outcome_results = []
    for train, test in folded_indices:
        #initialize the training and testing data sets according to fold indices
        train_x, test_x = set_x.iloc[train], set_x.iloc[test]
        train_y, test_y = set_y.iloc[train], set_y.iloc[test]

        #create an Machine Learning predictor object according to which algorithm was selected
        ML_predictor = None
        if validation_ML_algorithm == 'NN':
            ML_predictor = TaMERI_NN.neural_network()
        elif validation_ML_algorithm == 'RF':
            ML_predictor = TaMERI_RF.random_forest()
        #train the Machine Learning model
        ML_predictor.train(train_x, train_y)
        #calculate predictions with the trained Machine Learning model
        predictions = ML_predictor.predict(test_x)
        #calculate evaluation measurements of the predictions
        MAE, EVS, R2 = evaluate_predictions(predictions, test_y)
        #output the results of the current fold
        print("Fold " + str(current_fold) + " - " + "MAE: " + str(MAE))
        print("Fold " + str(current_fold) + " - " + "EVS: " + str(EVS))
        print("Fold " + str(current_fold) + " - " + "R2: " + str(R2))
        #save the predictions<->real of the current fold
        outcome_data.append((predictions, test_y, current_fold))
        outcome_results.append((current_fold, MAE, EVS, R2))
        #increase fold counter
        current_fold += 1
    #Dump data and results into files
    cv_results_dir = dump_results(outcome_data, outcome_results, validation_ML_algorithm)
    #Plot evaluation results for visualization
    plot_results(cv_results_dir, validation_ML_algorithm)

#Evaluate the predictions by comparing to the real values
def evaluate_predictions(pred, real):
    MAE = mean_absolute_error(real, pred)
    EVS = explained_variance_score(real, pred)
    R2 = r2_score(real, pred)
    return MAE,EVS,R2

#Dump the prediction data and results into files
def dump_results(data_list, result_list, validation_ML_algorithm):
    #IF validation result directory doesn't exist -> create it
    results_dir = os.path.join("data", "cv_results" + "." + validation_ML_algorithm)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    #Dump cross validation data
    cv_dataPATH = os.path.join(results_dir, "data.tsv")
    with open(cv_dataPATH, 'w') as data_dumper:
        #write header
        data_dumper.write("real" + "\t" + "pred" + "\t" + "fold" + "\n")
        #iterate over each saved fold_tuple
        for fold_tuple in data_list:
            #parse variables
            pred = fold_tuple[0]
            real = fold_tuple[1].tolist()
            fold = fold_tuple[2]
            #print data to file for each sample
            for i, p in enumerate(pred):
                data_dumper.write(str(real[i]) + "\t" + str(p) + "\t" + str(fold) + "\n")
    #Dump cross validation results
    cv_resultsPATH = os.path.join(results_dir, "scores.tsv")
    with open(cv_resultsPATH, 'w') as result_dumper:
        #write header
        result_dumper.write("fold" + "\t" + "MAE" + "\t" + "EVS" + "\t" + "R2" + "\n")
        #iterate over each saved fold_tuple
        for fold_tuple in result_list:
            #parse variables
            fold = fold_tuple[0]
            MAE = fold_tuple[1]
            EVS = fold_tuple[2]
            R2 = fold_tuple[3]
            #print results to file for each sample
            result_dumper.write(str(fold) + "\t" + str(MAE) + "\t" + str(EVS) + "\t" + str(R2) + "\n")
    return results_dir

#Plot evaluation via Rscript
def plot_results(cv_results_dir, validation_ML_algorithm):
    #Fixed parameter to Rscript
    rscript_path = os.path.abspath(os.path.join("scripts", "evaluate_Validation.R"))
    #Identify ML algorithm
    ML_algorithm = None
    if validation_ML_algorithm == "NN":
        ML_algorithm = "Neural Network"
    elif validation_ML_algorithm == "RF":
        ML_algorithm = "Random Forest"
    #Save and then change the current working directory into the cv_results directory
    original_wd = os.getcwd()
    os.chdir(cv_results_dir)
    #Run the Rscript
    out = subprocess.call(["Rscript", rscript_path, "./", ML_algorithm])
    #Return to original working directory
    os.chdir(original_wd)
