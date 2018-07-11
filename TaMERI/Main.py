#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
import argparse
import pandas as pd
from sklearn.metrics import classification_report,confusion_matrix

#-----------------------------------------------------#
#                  Parse command line                 #
#-----------------------------------------------------#
#Initialize argument parser
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=
    """TaMERI: TrAnsMembrane Evolutionary Rate Influence - Neural network predictor
Prediction of transmembrane influence on the evolutionary rate of membrane proteins through protein determinants.
Trained on AAIMON slopes from the Korbinian pipeline as representative for TM/EM ER ratios.

Author: Dominink Müller
Email: ga37xiy@tum.de
Lab: Frishman lab - TUM Weihenstephan (Germany)
""")
#Add arguments
parser.add_argument('-i', '--input', type=str, action='store', required=False, dest='args_input',
                    help='Path to a data set (UniProt flat file or TaMERI-input.tsv file)')
parser.add_argument('-t', '--train', type=str, action='store', required=False, dest='args_train',
                    help='Path to a training data set (TaMERI-input.tsv file)')
parser.add_argument('-c', '--calibrate', default=False, action='store_true', dest='args_calibration',
                    help='Boolean tag if the neural network parameters should be automatically calibrated depending on the\
                    provided training data set or fixed parameters should be used\
                    (which was selected by me as the best for this problem)')
#parser.add_argument('-o', '--filesystem', type=str, action='store', required=True, dest='args_filesystem',
#                    help='REQUIRED: Path where the filesystem (output) should be set up / stored (PDB database, results, temporary files, ...)')
#Parse arguments
args = parser.parse_args()

#-----------------------------------------------------#
#                     Parameters                      #
#-----------------------------------------------------#
#Path to input data for which predictions should be calculated
path_inputData = args.args_input
#Path to training data for which a own neural network model can be trained
path_trainingData = args.args_train
#Boolean tag, if the neural network parameter should be automatically calibrated depending on the training data set
boolean_calibration = args.args_calibration

#-----------------------------------------------------#
#                    Runner code                      #
#-----------------------------------------------------#
#Read data set
import InputReader as IR
mpg_dataset = IR.read_TestSet("data/mpg.tsv")

#preprocess data
import Preprocessing as PC
x, y = PC.prepare_data(mpg_dataset)
x = PC.one_hot_encoder(x, [6])

#create the neural network
import NeuralNetwork as NN
#NN.train_model(x,y)

NN.calibrate_model_parameter(x,y)

#NN.train_model(x_train, y_train, (6,6), 1000)
#
# #use trained neural network to predict test data set
# predictions = NN.predict(x_test)
#
# #evaluate predictions
# real = y_test.tolist()
# for i, pred in enumerate(predictions):
#     print(str(pred) + "\t" + str(real[i]) + "\t" + str(pred-real[i]))
#
# # #evaluate predictions
# # #print(confusion_matrix(y_test,predictions))
# # #print(classification_report(y_test,predictions))
