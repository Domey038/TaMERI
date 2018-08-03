#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
#External libraries
import sys
import argparse
import pandas as pd
#TaMERI libraries/scripts
import InputReader as TaMERI_IR
import Preprocessing as TaMERI_PC
import Validation as TaMERI_VAL
import NeuralNetwork as TaMERI_NN
import RandomForest as TaMERI_RF

#-----------------------------------------------------#
#                  Parse command line                 #
#-----------------------------------------------------#
#Implement a modified ArgumentParser from the argparse package
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message + "\n")
        self.print_help()
        sys.exit(2)
#Initialize the modifed argument parser
parser = MyParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False, description=
    """TaMERI: TrAnsMembrane Evolutionary Rate Influence - Machine learning predictor
Prediction of transmembrane influence on the evolutionary rate of membrane proteins through protein determinants.
Trained on AAIMON slopes from the Korbinian pipeline as representative for TM/EM ER ratios.

Example usage:
python TaMERI/main.py -t data/training_set.TaMERI.tsv -c
python TaMERI/main.py -p data/test_set.TaMERI.tsv
python TaMERI/main.py -v data/test_set.TaMERI.tsv

Author: Dominink Müller
Email: ga37xiy@tum.de
Lab: Dmitrij Frishman lab - TUM Weihenstephan (Germany)
""")
#Add arguments for mutally exclusive required group
required_group = parser.add_argument_group(title='TaMERI modi')
exclusive_args = required_group.add_mutually_exclusive_group(required=True)
exclusive_args.add_argument('-p', '--predict', type=str, action='store', required=False, dest='args_predict',
                    help='Path to a prediction data set (UniProt flat file or TaMERI-input.tsv file)')
exclusive_args.add_argument('-t', '--train', type=str, action='store', required=False, dest='args_train',
                    help='Path to a training data set (TaMERI-input.tsv file)')
exclusive_args.add_argument('-v', '--validate', type=str, action='store', required=False, dest='args_validate',
                    help='Path to a data set (TaMERI-input.tsv file).\
                    Execute a 5-fold cross-validation with 4/5 training and 1/5 testing data set size.\
                    Outputs evaluation results.')
#Add arguments for the machine learning algorithm group
mla_group_fw = parser.add_argument_group(title='Machine learning algorithm')
mla_group = mla_group_fw.add_mutually_exclusive_group(required=False)
mla_group.add_argument('-NN', '--neural_network', default=False, action='store_true', dest='args_MLA_NN',
                    help='Boolean variable, if a neural network algorithm should be used (DEFAULT)')
mla_group.add_argument('-RF', '--random_forest', default=False, action='store_true', dest='args_MLA_RF',
                    help='Boolean variable, if a random forest algorithm should be used')
#Add arguments for optional group
optional_group = parser.add_argument_group(title='Optional arguments')
optional_group.add_argument('-c', '--calibrate', default=False, action='store_true', dest='args_calibration',
                    help='Boolean tag, if the neural network parameters should be automatically calibrated depending on the\
                    provided training data set (instead of using TaMERI\'s fixed parameters).\
                    Only affect the training modus.\
                    WARNING: It is NOT recommended to use this argument if your data set isn\'t sufficient for training.')
optional_group.add_argument('-m', '--model', type=str, action='store', required=False, dest='args_model',
                    help='NOT IMPLEMENTED YET!\
                    Use a external/own neural network model instead of using the model provided by TaMERI.\
                    If using the -train or -validate command, the external model will be ignored!')
#parser.add_argument('-o', '--filesystem', type=str, action='store', required=True, dest='args_filesystem',
#                    help='REQUIRED: Path where the filesystem (output) should be set up / stored\
#                   (PDB database, results, temporary files, ...)')
optional_group.add_argument('-h', '--help', action="help", help="Show this help message and exit")
#Parse arguments
args = parser.parse_args()

#-----------------------------------------------------#
#                     Parameters                      #
#-----------------------------------------------------#
#Path to prediction data for which predictions should be calculated
path_predictionData = args.args_predict
#Path to training data for which a own neural network model can be trained
path_trainingData = args.args_train
#Path to data set for evaluate prediction power with a 5-fold cross-validation
path_validationData = args.args_validate

#Boolean tag, if the neural network parameter should be automatically calibrated depending on the training data set
boolean_calibration = args.args_calibration

#Define which machine learning algorithm should be used for validation
#NN = Neural Network; RF = Random Forest - DEFAULT = NN
validation_ML_algorithm = 'NN'
if args.args_MLA_NN:
    validation_ML_algorithm = 'NN'
elif args.args_MLA_RF:
    validation_ML_algorithm = 'RF'

#-----------------------------------------------------#
#                    Runner code                      #
#-----------------------------------------------------#
############################
#         Training         #
############################
if path_trainingData != None:
    #Read data set in TaMERI-input.tsv format (AAIMON slopes have to be provided)
    data_set = TaMERI_IR.read_TaMERI_tsv(path_trainingData)
    #data_set = TaMERI_IR.read_r4s_tsv(path_trainingData)
    #Preprocessing: Remove non-finite results
    data_set = TaMERI_PC.clean_data(data_set)
    #Preprocessing: Split data and results of the data set
    set_x, set_y = TaMERI_PC.split_data_from_results(data_set, "ER_ratio")
    #Preprocessing: Transform categorical features into dummy variables
    set_x = TaMERI_PC.create_dummy_variables(set_x, ['C', 'F', 'P', 'uniprot_KWs'])
    #Preprocessing: Create and fit data through standard scaling
    TaMERI_PC.create_fitting(set_x)
    set_x = TaMERI_PC.fit_data(set_x)
    #Create a ML predictor model
    ML_predictor = None
    if validation_ML_algorithm == "NN":
        ML_predictor = TaMERI_NN.neural_network()
    elif validation_ML_algorithm == "RF":
        ML_predictor = TaMERI_RF.random_forest()
    if not boolean_calibration:
        #Train the ML predictor model with all of provided data
        ML_predictor.train(set_x, set_y)
    else:
        #Calibrate the ML predictor model to find best parameters
        ML_predictor.calibrate(set_x, set_y)
    #Dump the trained ML predictor model for later usage/prediction
    ML_predictor.dump()

############################
#        Prediction        #
############################
elif path_predictionData != None:
    #Read data set in TaMERI-input.tsv format or in an UniProt flat file format
    data_set = TaMERI_IR.read_TaMERI_tsv(path_predictionData)
    #Preprocessing: Transform categorical features into dummy variables
    data_set = TaMERI_PC.create_dummy_variables(data_set, ['C', 'F', 'P', 'uniprot_KWs'])
    #Preprocessing: Fit the data through the saved standard scaling
    data_set = TaMERI_PC.fit_data(data_set)
    #Create a ML predictor model object
    ML_predictor = None
    if validation_ML_algorithm == "NN":
        ML_predictor = TaMERI_NN.neural_network()
    elif validation_ML_algorithm == "RF":
        ML_predictor = TaMERI_RF.random_forest()
    #Load the previously trained ML predictor model from disk
    ML_predictor.load()
    #Calculate predictions with the ML predictor model
    predictions = ML_predictor.predict(data_set)
    #Output the predictions to console
    print(predictions)

############################
#        Validation        #
############################
elif path_validationData != None:
    #Read data set in TaMERI-input.tsv format (AAIMON slopes have to be provided)
    data_set = TaMERI_IR.read_TaMERI_tsv(path_validationData)
    #data_set = TaMERI_IR.read_r4s_tsv(path_validationData)
    #Preprocessing: Remove non-finite results
    data_set = TaMERI_PC.clean_data(data_set)
    #Preprocessing: Split data and results of the data set
    set_x, set_y = TaMERI_PC.split_data_from_results(data_set, "ER_ratio")
    #Preprocessing: Transform categorical features into dummy variables
    set_x = TaMERI_PC.create_dummy_variables(set_x, ['C', 'F', 'P', 'uniprot_KWs'])
    #Preprocessing: Create and fit data through standard scaling
    TaMERI_PC.create_fitting(set_x)
    set_x = TaMERI_PC.fit_data(set_x)
    #Validate TaMERI through a 5-fold cross-validation
    TaMERI_VAL.cross_validation(set_x, set_y, validation_ML_algorithm)
