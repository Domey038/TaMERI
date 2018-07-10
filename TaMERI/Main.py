#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
import pandas as pd
from sklearn.metrics import classification_report,confusion_matrix

#-----------------------------------------------------#
#                  Parse command line                 #
#-----------------------------------------------------#
#TODO: argparse


#-----------------------------------------------------#
#                    Runner code                      #
#-----------------------------------------------------#
#Read data
import InputReader as IR
mpg_dataset = IR.read_TestSet("data/mpg.tsv")

#preprocess data
import Preprocessing as PC
x, y = PC.prepare_data(mpg_dataset)
x = PC.one_hot_encoder(x, [6])
x_train, x_test, y_train, y_test = PC.split_data(x,y)
PC.create_fitting(x_train)
x_train = PC.fit_data(x_train)
x_test = PC.fit_data(x_test)

#create the neural network
import NeuralNetwork as NN
NN.train_model(x_train, y_train)

#use trained neural network to predict test data set
predictions = NN.predict(x_test)

#evaluate predictions
real = y_test.tolist()
for i, pred in enumerate(predictions):
    print(str(pred) + "\t" + str(real[i]) + "\t" + str(pred-real[i]))

# #evaluate predictions
# #print(confusion_matrix(y_test,predictions))
# #print(classification_report(y_test,predictions))
