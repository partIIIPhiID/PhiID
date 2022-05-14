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
timechunks = ['pre1', 'pre2', 'post1', 'post2']
elec_list = pd.read_csv('rand_electrode_list.csv')
N = 500
elecA = int(elec_list.loc[0].at['electrode A'])
elecB = int(elec_list.loc[0].at['electrode B'])
for chunk in timechunks:
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
    for atom in atoms:
        metric = pd.DataFrame(columns = ['predicted_value', 'actual_value', 'drowsiness'])
        metric1 = pd.DataFrame(columns = ['predicted_value', 'actual_value', 'drowsiness'])
        metric2 = pd.DataFrame(columns = ['predicted_value', 'actual_value', 'drowsiness'])
        metric3 = pd.DataFrame(columns = ['predicted_value', 'actual_value', 'drowsiness'])
        metrics = [metric1, metric2, metric3]
        truth_tables = [None, None, None]
        for i in range(0,2):
            drowsy_level = drowsy_levels[i]
            data_forLDA = data[data['drowsiness'] == f'{drowsy_level}']   
            data_forLDA = data_forLDA.reset_index(drop=True)
            x = np.transpose([data_forLDA[f'{atom}']])
            y = data_forLDA['performance'].replace({'hit': 1, 'miss': 0})
            #take 80% of trials to train with and 20% of trials to predict with
            learning_trials = random.sample(range(1, len(y)), math.floor(0.8*len(y)))
            predicting_trials =  list(set(range(1, len(y))) - set(learning_trials))
            learning_x = [x[j] for j in learning_trials]
            learning_y = [y[j] for j in learning_trials]
            predicting_x = [x[j] for j in predicting_trials]
            predicting_y = [y[j] for j in predicting_trials]
            clf = LinearDiscriminantAnalysis()
            clf.fit(learning_x, learning_y)
            metrics[i]['predicted_value'] = clf.predict(predicting_x)
            metrics[i]['actual_value'] = predicting_y
            metrics[i]['drowsiness'] = metrics[i]['drowsiness'].fillna(f'{drowsy_level}')
            metric = pd.concat([metric, metrics[i]])
            truth_tables[i] = pd.crosstab(metrics[i]['predicted_value'], metrics[i]['actual_value'])
            predictive_strength = (truth_tables[i].loc[0, 0] + truth_tables[i].loc[1, 1])/(truth_tables[i].loc[0, 0] + truth_tables[i].loc[1, 1] + truth_tables[i].loc[0, 1] + truth_tables[i].loc[1, 0])
            print(atom)
            print(chunk)
            print(predictive_strength)
        del metric1, metric2, metric3
        del truth_tables