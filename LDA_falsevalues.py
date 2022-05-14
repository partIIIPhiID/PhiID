# -*- coding: utf-8 -*-
"""
Created on Mon May  2 13:37:00 2022

@author: andre
"""




import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import sys
atom = 'rtr'
atoms = ["rtx", "rty", "rts", "str", "stx", "sty", "sts", "xtr", "xtx", "xty", "xts", "ytr", "ytx","yty", "yts"] #we run through the first atom, rtr, slightly differently, so it's excluded from this list
chunk = 'pre2'
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
    
drowsy_levels = ['awake', 'light drowsy', 'heavy drowsy']
metric = pd.DataFrame(columns = ['predicted_value', 'actual_value', 'drowsiness'])
metric1 = pd.DataFrame(columns = ['predicted_value', 'actual_value', 'drowsiness'])
metric2 = pd.DataFrame(columns = ['predicted_value', 'actual_value', 'drowsiness'])
metric3 = pd.DataFrame(columns = ['predicted_value', 'actual_value', 'drowsiness'])
df_list = [metric1, metric2, metric3]
for i in range(0,2):
    drowsy_level = drowsy_levels[i]
    data_forLDA = data[data['drowsiness'] == f'{drowsy_level}']   
    data_forLDA = data_forLDA.reset_index(drop=True)
    x = np.transpose([data_forLDA['rtr'], data_forLDA['rtx'], data_forLDA['rty'], data_forLDA['rts'], 
    data_forLDA['xtr'], data_forLDA['xtx'], data_forLDA['xty'], data_forLDA['xts'], 
    data_forLDA['rtr'], data_forLDA['rtx'], data_forLDA['yty'], data_forLDA['yts'],
    data_forLDA['str'], data_forLDA['stx'], data_forLDA['sty'], data_forLDA['sts']])
    y = data_forLDA['performance']
    clf = LinearDiscriminantAnalysis()
    clf.fit(x, y)
    df_list[i]['predicted_value'] = np.sign(clf.decision_function(x))
    df_list[i]['actual_value'] = data_forLDA['performance']
    #rough_analysis_performance = rough_analysis_performance.replace(['hit', 'miss'], [1, -1])
    #rough_analysis_performance = rough_analysis_performance.replace(['hit', 'miss'], [1, -1])
    df_list[i]['drowsiness'] = df_list[i]['drowsiness'].fillna(f'{drowsy_level}')
    metric = pd.concat([metric, df_list[i]])
    truth_table = pd.crosstab(df_list[i]['predicted_value'], df_list[i]['actual_value'])