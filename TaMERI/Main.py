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
    """TaMERI: TrAnsMembrane Evolutionary Rate Influence - Neural network predictor
Prediction of transmembrane influence on the evolutionary rate of membrane proteins through protein determinants.
Trained on AAIMON slopes from the Korbinian pipeline as representative for TM/EM ER ratios.

Author: Dominink Müller
Email: ga37xiy@tum.de
Lab: Frishman lab - TUM Weihenstephan (Germany)
""")
#Add arguments for mutally exclusive required group
required_group = parser.add_argument_group(title='Required + mutally exclusive arguments')
exclusive_args = required_group.add_mutually_exclusive_group(required=True)
exclusive_args.add_argument('-i', '--input', type=str, action='store', required=False, dest='args_input',
                    help='Path to a data set (UniProt flat file or TaMERI-input.tsv file)')
exclusive_args.add_argument('-t', '--train', type=str, action='store', required=False, dest='args_train',
                    help='Path to a training data set (TaMERI-input.tsv file)')
exclusive_args.add_argument('-v', '--validate', type=str, action='store', required=False, dest='args_validate',
                    help='Execute a 5-fold cross-validation with 4/5 training and 1/5 testing data set size.\
                    Outputs evaluation results.\
                    Path to a data set (TaMERI-input.tsv file)')
#Add arguments for optional group
optional_group = parser.add_argument_group(title='Optional arguments')
# optional_group.add_argument('-c', '--calibrate', default=False, action='store_true', dest='args_calibration',
#                     help='Boolean tag if the neural network parameters should be automatically calibrated depending on the\
#                     provided training data set or fixed parameters should be used\
#                     (which was selected by me as the best for this problem)')
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
#Path to input data for which predictions should be calculated
path_inputData = args.args_input
#Path to training data for which a own neural network model can be trained
path_trainingData = args.args_train
#Path to data set for evaluate prediction power with a 5-fold cross-validation
path_validationData = args.args_validate
#Boolean tag, if the neural network parameter should be automatically calibrated depending on the training data set
#boolean_calibration = args.args_calibration
boolean_calibration = False

#-----------------------------------------------------#
#                    Runner code                      #
#-----------------------------------------------------#
############################
#         Training         #
############################
if path_inputData != None:
    sys.exit(0)
#Training
#IF TRAINING==TRUE/was choosen
#-> read training data set
#-> preprocess training data set
#-> IF calibrate==TRUE -> calibrate
#-> Train with fixed/calibrated values
#ELSE
#-> use existing model+scaling

############################
#        Prediction        #
############################
elif path_trainingData != None:
    sys.exit(0)
#Prediction
#ELSE_IF PREDICTION==TRUE/was choosen
#-> read input data / parse Uniprot format into TaMERI tsv
#-> preprocess (scale) data
#-> use existing model for

############################
#        Validation        #
############################
elif path_validationData != None:
    #Read data set in TaMERI-input.tsv format (AAIMON slopes have to be provided)
    #data_set = IR.read_TaMERI_tsv(path_validationData)
    data_set = TaMERI_IR.read_TestSet(path_validationData)
    #Preprocessing: Split data and results of the data set
    set_x, set_y = TaMERI_PC.split_data_from_results(data_set, "mpg")
    #Preprocessing: Transform categorical features via OHE
    set_x = TaMERI_PC.one_hot_encoder(set_x, [6])
    #Preprocessing: Create and fit data through standard scaling
    TaMERI_PC.create_fitting(set_x)
    set_x = TaMERI_PC.fit_data(set_x)
    #Validate TaMERI through a 5-fold cross-validation
    TaMERI_VAL.cross_validation(set_x, set_y)




# #Prediction
# mpg_dataset = IR.read_TestSet("data/mpg.tsv")
#
# #preprocess data
# x, y = PC.prepare_data(mpg_dataset)
# x = PC.one_hot_encoder(x, [6])
#
# #create the neural network
# import NeuralNetwork as NN
# #NN.train_model(x,y)
#
# NN.calibrate_model_parameter(x,y)
