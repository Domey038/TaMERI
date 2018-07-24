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

#-----------------------------------------------------#
#               Testing / Debugging code              #
#-----------------------------------------------------#
#path = "/home/domey/Studium-Shit/Master/SS_2018/Masterarbeit/working_dir/data/uniprot/swissprot.drosophila_melanogaster.txt"
#TaMERI_IR.read_UniProt(path)

path = "/home/domey/Studium-Shit/Master/SS_2018/Masterarbeit/working_dir/TaMERI/data/homo_sapiens.TaMERI_withGO.tsv"
df = TaMERI_IR.read_TaMERI_tsv(path)
df = TaMERI_PC.create_dummy_variables(df, ['C', 'F', 'P'])
print(df)

#TODO
#preprocessing add one-hot-encoding / dummy variable creation
#https://stackoverflow.com/questions/43945816/convert-list-of-strings-to-dummy-variables-with-pandas

#"set()" in data frame -> replace with [] or {}
