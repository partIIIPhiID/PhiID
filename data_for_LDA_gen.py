# -*- coding: utf-8 -*-
"""
Created on Mon May  2 11:32:16 2022

@author: andre
"""



import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import sys
import random
import math


atom = 'rtr'
atoms = ["rtx", "rty", "rts", "str", "stx", "sty", "sts", "xtr", "xtx", "xty", "xts", "ytr", "ytx","yty", "yts"] #we run through the first atom, rtr, slightly differently, so it's excluded from this list
chunk = 'post2'
elec_list = pd.read_csv('rand_electrode_list.csv')
N = 500
elecA = int(elec_list.loc[0].at['electrode A'])
elecB = int(elec_list.loc[0].at['electrode B'])
df = pd.read_csv(f'performance_data_cross_{elecA}{elecB}_{atom}_{chunk}.csv')
df = df.rename(columns = {'metric':f'{elecA}{elecB}'})
for n_i in range(1,499):
        try:
            elecA = int(elec_list.loc[n_i].at['electrode A'])
            elecB = int(elec_list.loc[n_i].at['electrode B'])
            df_temp = pd.read_csv(f'performance_data_cross_{elecA}{elecB}_{atom}_{chunk}.csv')
            df[f'{elecA}{elecB}'] = df_temp['metric']
        except:
            print(f'missing data for {n_i}')
df['mean'] = df.mean(axis=1)
data = df[['drowsiness','performance','mean']] #here we initialise the dataframe that we will add each atom to and then perform an LDA with
data = data.rename(columns = {'mean':'rtr'})

for atom in atoms:
    elecA = int(elec_list.loc[0].at['electrode A'])
    elecB = int(elec_list.loc[0].at['electrode B'])
    df = pd.read_csv(f'performance_data_cross_{elecA}{elecB}_{atom}_{chunk}.csv')
    df = df.rename(columns = {'mean':f'{elecA}{elecB}'})
    for n_i in range(1,499):
            try:
                elecA = int(elec_list.loc[n_i].at['electrode A'])
                elecB = int(elec_list.loc[n_i].at['electrode B'])
                df_temp = pd.read_csv(f'performance_data_cross_{elecA}{elecB}_{atom}_{chunk}.csv')
                df[f'{elecA}{elecB}'] = df_temp['metric']
            except:
                print(f'missing data for {n_i}')
    df['mean'] = df.mean(axis=1)
    data[f'{atom}'] = df['mean']
data.to_csv(f'mean_{chunk}_data.csv')