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
import Validation as TaMERI_VAL

#-----------------------------------------------------#
#               Testing / Debugging code              #
#-----------------------------------------------------#
#
# input_nodes = 50
# diff_range = 50
# step = 2
#
# HL_list = set()
# for i in range(max(0, input_nodes-diff_range), input_nodes+diff_range, step):
#     for j in range(max(0, input_nodes-diff_range), input_nodes+diff_range, step):
#         HL_list.add((i,j))
#     HL_list.add((i,))
# HL_list = list(HL_list)
# print(HL_list)
#     # ranges = [(n, min(n+step, stop)) for n in range(start, stop, step)]
#     # print(ranges)
# import InputReader as TaMERI_IR
# import Preprocessing as TaMERI_PC
# import Validation as TaMERI_VAL
# import NeuralNetwork as TaMERI_NN
# import RandomForest as TaMERI_RF
# path_validationData = "/home/domey/Studium-Shit/Master/SS_2018/Masterarbeit/working_dir/TaMERI/data/auto-mpg.tsv"
# data_set = TaMERI_IR.read_TestSet(path_validationData)
# #data_set = TaMERI_PC.clean_data(data_set)
# set_x, set_y = TaMERI_PC.split_data_from_results(data_set, "mpg")
# #set_x = TaMERI_PC.create_dummy_variables(set_x, ['C', 'F', 'P'])
# TaMERI_PC.create_fitting(set_x)
# set_x = TaMERI_PC.fit_data(set_x)
# #TaMERI_VAL.cross_validation(set_x, set_y, "RF")
#
#
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import GridSearchCV
# from sklearn.model_selection import KFold
# crva = KFold(n_splits=3)
#
# model = RandomForestRegressor(random_state=0)
#
# param_grid = {"n_estimators": [100],
#     "max_depth": [None],
#     "max_features": ['sqrt'],
#     "min_samples_split": [2],
#     "min_samples_leaf": [1],
#     "bootstrap": [False]}
# clf = GridSearchCV(model, param_grid, cv=crva, scoring='r2', n_jobs=-1)
# clf.fit(set_x,set_y)
# print(clf.cv_results_['split0_test_score'])
# print(clf.cv_results_['split1_test_score'])
# print(clf.cv_results_['split2_test_score'])
#
# from sklearn.metrics import r2_score
# model = RandomForestRegressor(random_state=0, n_estimators=100, max_depth=None,
#                                     min_samples_split=2, min_samples_leaf=1, max_features='sqrt',
#                                     bootstrap=False)
#
# from sklearn.model_selection import cross_val_score
# scores = cross_val_score(model, set_x, set_y, cv=crva, scoring='r2')
# print(scores)

#
# y_pred = cross_val_predict(model, set_x, set_y, cv=cv)
# r2 = r2_score(y_pred = y_pred, y_true = set_y)
# print(r2)
#
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(set_x, set_y, test_size=0.10, random_state=0)
# model.fit(X_train, y_train)
# r2 = r2_score(y_pred = model.predict(X_test), y_true = y_test)
# print(r2)

#-----------------------------------------------------#
#              Create Mark test data set              #
#-----------------------------------------------------#
from ast import literal_eval
import itertools

# path_cr_csv = "/home/domey/Studium-Shit/Master/SS_2018/Masterarbeit/working_dir/testing_area/TaMERI_dataset/11/List11_cr_summary.csv"
# data_set = pd.read_csv(path_cr_csv, sep=",")
# TaMERI_df = data_set[['protein_name', 'AAIMON_slope_all_TMDs_mean', 'number_of_TMDs']]
# # TaMERI_df = data_set[['protein_name', 'AAIMON_slope_all_TMDs_mean', 'number_of_TMDs', 'AAIMON_n_homol',
# #                   'TM01_SW_q_gaps_per_q_residue_mean', 'obs_changes_mean']]

path_simple_csv = "/home/domey/Studium-Shit/Master/SS_2018/Masterarbeit/working_dir/testing_area/TaMERI_dataset/11/List11.csv"
korbinian_df = pd.read_csv(path_simple_csv, sep=",", low_memory=False)

print(korbinian_df['comments_subcellular_location_uniprot'])

#
# def get_major_keywords(in_series, min_proteins_with_keyword):
#     """Get list of major keywords from pandas series.
#     Adapted from korbinian.cons_ratios.keywords.py
#     """
#     # join all keywords together into a large list
#     nested_list_all_KW = list(itertools.chain(*list(in_series.dropna())))
#     # convert list to pandas series
#     all_KW_series = pd.Series(nested_list_all_KW)
#     # obtain series of major keywords
#     KW_counts = all_KW_series.value_counts()
#     # exclude keywords with less than x applicable proteins
#     cutoff_major_keywords = min_proteins_with_keyword
#     KW_counts_major = KW_counts[KW_counts > cutoff_major_keywords]
#     # extract series indices and make them a python list
#     list_KW_counts_major = sorted(list(KW_counts_major.index))
#     return list_KW_counts_major

# list_KW_counts_major = get_major_keywords(data_set['uniprot_KW_list'], 10)
# list_ignored_KW = ['Transmembrane', 'Complete proteome', 'Reference proteome', 'Membrane','Transmembrane helix']
# for kw in list_ignored_KW:
#     if kw in list_KW_counts_major:
#         list_KW_counts_major.remove(kw)
#
# df_kw = pd.DataFrame()
# for kw in list_KW_counts_major:
#     df_kw[kw] = data_set['uniprot_KW'].str.contains(kw)
# df_kw = df_kw.fillna(0).astype(int)
#
# data_set['comments_subcellular_location_uniprot_list'] = data_set['comments_subcellular_location_uniprot'].dropna().apply(
#                                                         lambda x : x.split("; "))
# list_locations_counts_major = get_major_keywords(data_set['comments_subcellular_location_uniprot_list'], 20)
# df_locations = pd.DataFrame()
# for location in list_locations_counts_major:
#     df_locations[location] = data_set['comments_subcellular_location_uniprot'].str.contains(location)
#
# TaMERI_df = pd.concat([df_kw, temporary_df, TaMERI_df, df_locations], axis=1)
# TaMERI_df.to_csv("data/TaMERI.test_dataset.mark_noSeqVar.tsv", sep="\t", index=False, header=True)


























# path_cr_csv = "/home/domey/Studium-Shit/Master/SS_2018/Masterarbeit/working_dir/testing_area/TaMERI_dataset/11/List11_cr_summary.csv"
# data_set = pd.read_csv(path_cr_csv, sep=",")
# TaMERI_df = data_set[['protein_name', 'AAIMON_slope_all_TMDs_mean', 'number_of_TMDs']]
# # TaMERI_df = data_set[['protein_name', 'AAIMON_slope_all_TMDs_mean', 'number_of_TMDs', 'AAIMON_n_homol',
# #                   'TM01_SW_q_gaps_per_q_residue_mean', 'obs_changes_mean']]
#
# path_simple_csv = "/home/domey/Studium-Shit/Master/SS_2018/Masterarbeit/working_dir/testing_area/TaMERI_dataset/11/List11.csv"
# korbinian_df = pd.read_csv(path_simple_csv, sep=",", low_memory=False)
# #data_set = TaMERI_df.merge(data_set, left_on='protein_name', right_on='protein_name', how='inner')
# useful_cols = ["protein_name", "multipass", "number_of_SP", "seqlen",
#                "singlepass", "typeI", "typeII", "TM01_start",
#                "perc_TMD", "len_TMD_mean", "TM01_lipo",
#                "lipo_mean_all_TM_res", "lipo_last_TMD",
#                "Cell_membrane", "Endoplasmic_reticulum", "Golgi_apparatus",
#                "GPCR", "olfactory_receptor"]
# temporary_df = data_set[useful_cols]
# #
# TaMERI_df = TaMERI_df.rename(columns={'protein_name': 'id', 'AAIMON_slope_all_TMDs_mean': 'ER_ratio',
#                    'number_of_TMDs': 'TM_regions'}, inplace=False)
#
# data_set['uniprot_KW_list'] = data_set['uniprot_KW'].dropna().apply(literal_eval)
#
# def get_major_keywords(in_series, min_proteins_with_keyword):
#     """Get list of major keywords from pandas series.
#     Adapted from korbinian.cons_ratios.keywords.py
#     """
#     # join all keywords together into a large list
#     nested_list_all_KW = list(itertools.chain(*list(in_series.dropna())))
#     # convert list to pandas series
#     all_KW_series = pd.Series(nested_list_all_KW)
#     # obtain series of major keywords
#     KW_counts = all_KW_series.value_counts()
#     # exclude keywords with less than x applicable proteins
#     cutoff_major_keywords = min_proteins_with_keyword
#     KW_counts_major = KW_counts[KW_counts > cutoff_major_keywords]
#     # extract series indices and make them a python list
#     list_KW_counts_major = sorted(list(KW_counts_major.index))
#     return list_KW_counts_major
#
# list_KW_counts_major = get_major_keywords(data_set['uniprot_KW_list'], 10)
# list_ignored_KW = ['Transmembrane', 'Complete proteome', 'Reference proteome', 'Membrane','Transmembrane helix']
# for kw in list_ignored_KW:
#     if kw in list_KW_counts_major:
#         list_KW_counts_major.remove(kw)
#
# df_kw = pd.DataFrame()
# for kw in list_KW_counts_major:
#     df_kw[kw] = data_set['uniprot_KW'].str.contains(kw)
# df_kw = df_kw.fillna(0).astype(int)
#
# data_set['comments_subcellular_location_uniprot_list'] = data_set['comments_subcellular_location_uniprot'].dropna().apply(
#                                                         lambda x : x.split("; "))
# list_locations_counts_major = get_major_keywords(data_set['comments_subcellular_location_uniprot_list'], 20)
# df_locations = pd.DataFrame()
# for location in list_locations_counts_major:
#     df_locations[location] = data_set['comments_subcellular_location_uniprot'].str.contains(location)
#
# TaMERI_df = pd.concat([df_kw, temporary_df, TaMERI_df, df_locations], axis=1)
# TaMERI_df.to_csv("data/TaMERI.test_dataset.mark_noSeqVar.tsv", sep="\t", index=False, header=True)
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
