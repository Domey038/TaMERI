#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
#External libraries
import sys
import argparse
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
#TaMERI libraries/scripts
import InputReader as TaMERI_IR

#-----------------------------------------------------#
#               Testing / Debugging code              #
#-----------------------------------------------------#





#-----------------------------------------------------#
#          Random forest on auto-mpg test set         #
#-----------------------------------------------------#
# path = "/home/domey/Studium-Shit/Master/SS_2018/Masterarbeit/working_dir/TaMERI/data/auto-mpg.tsv"
# df = TaMERI_IR.read_TestSet(path)
#
# set_x = df.drop('mpg', axis=1)
# set_y = df['mpg']
#
# scaler = StandardScaler()
# scaler.fit(set_x)
# set_x = scaler.transform(set_x)
#
# train_x, test_x, train_y, test_y = train_test_split(set_x, set_y)
#
# model = RandomForestRegressor(max_depth=2, random_state=0)
# model.fit(train_x, train_y)
#
# predictions = model.predict(test_x)
#
# MAE = mean_absolute_error(test_y, predictions)
# R2 = r2_score(test_y, predictions)
#
# print("MAE: " + str(MAE))
# print("R2: " + str(R2))
# print(model.feature_importances_)
