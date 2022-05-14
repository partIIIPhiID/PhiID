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
import statistics

atom = 'rtr'
atoms = ["rtx", "rty", "rts", "str", "stx", "sty", "sts", "xtr", "xtx", "xty", "xts", "ytr", "ytx","yty", "yts"] #we run through the first atom, rtr, slightly differently, so it's excluded from this list
chunks = ['pre1', 'pre2', 'post1', 'post2']  
drowsy_levels = ['awake', 'light drowsy', 'heavy drowsy']
N = 1000
df_p = pd.DataFrame(columns = ['Accuracy', 'Strategy' , 'Time period', 'Drowsiness'], index=range(N*24))
for k in range(0,4):
    chunk = chunks[k]
    predictive_strength_super = [None]*N
    guess_strength_super = [None]*N
    metric = pd.DataFrame(columns = ['predicted_value', 'actual_value', 'drowsiness'])
    metric1 = pd.DataFrame(columns = ['predicted_value', 'actual_value', 'drowsiness'])
    metric2 = pd.DataFrame(columns = ['predicted_value', 'actual_value', 'drowsiness'])
    metric3 = pd.DataFrame(columns = ['predicted_value', 'actual_value', 'drowsiness'])
    metrics = [metric1, metric2, metric3]
    truth_tables = [None, None, None]
    weight_vectors = [None, None, None]
    predictive_strength = [None, None, None]
    guess_strength = [None, None, None]
    data = pd.read_csv(f'mean_{chunk}_data.csv')
    for j in range(0, N):
        for i in range(0,3):
            drowsy_level = drowsy_levels[i]
            data_forLDA = data[data['drowsiness'] == f'{drowsy_level}']   
            data_forLDA = data_forLDA.reset_index(drop=True)
            x = np.transpose([data_forLDA['rts'], 
            data_forLDA['xts'], 
            data_forLDA['yts'],
            data_forLDA['str'], data_forLDA['stx'], data_forLDA['sty'], data_forLDA['sts']])
            y = data_forLDA['performance'].replace({'hit': 1, 'miss': 0})
            #take 80% of trials to train with and 20% of trials to predict with
            learning_trials = random.sample(range(1, len(y)), math.floor(0.8*len(y)))
            predicting_trials =  list(set(range(1, len(y))) - set(learning_trials))
            learning_x = [x[j] for j in learning_trials]
            learning_y = [y[j] for j in learning_trials]
            predicting_x = [x[j] for j in predicting_trials]
            predicting_y = [y[j] for j in predicting_trials]
            clf = LinearDiscriminantAnalysis(solver = 'lsqr')
            clf.fit(learning_x, learning_y)
            metrics[i]['predicted_value'] = clf.predict(predicting_x)
            metrics[i]['actual_value'] = predicting_y
            metrics[i]['drowsiness'] = metrics[i]['drowsiness'].fillna(f'{drowsy_level}')
            metric = pd.concat([metric, metrics[i]])
            truth_tables[i] = pd.crosstab(metrics[i]['predicted_value'], metrics[i]['actual_value'])
            predictive_strength[i] = (truth_tables[i].loc[0, 0] + truth_tables[i].loc[1, 1])/(truth_tables[i].loc[0, 0] + truth_tables[i].loc[1, 1] + truth_tables[i].loc[0, 1] + truth_tables[i].loc[1, 0])
            guess_strength[i] = (truth_tables[i].loc[0, 0] + truth_tables[i].loc[1, 0])/(truth_tables[i].loc[0, 0] + truth_tables[i].loc[1, 1] + truth_tables[i].loc[0, 1] + truth_tables[i].loc[1, 0])
            if guess_strength[i] < 0.5:
                guess_strength[i] = 1 - guess_strength[i]
            weight_vectors[i] = clf.coef_
        predictive_strength_super[j] = predictive_strength.copy()
        guess_strength_super[j] = guess_strength.copy()
    
    for j in range(0, N):
        df_p['Accuracy'][j + 3*N*k] = predictive_strength_super[j][0]
        df_p['Drowsiness'][j + 3*N*k] = 'awake'
        df_p['Accuracy'][j + N + 3*N*k] = predictive_strength_super[j][1]
        df_p['Drowsiness'][j + N + 3*N*k] = 'light drowsy'
        df_p['Accuracy'][j + 2*N + 3*N*k] = predictive_strength_super[j][2]
        df_p['Drowsiness'][j + 2*N + 3*N*k] = 'heavy drowsy'
        df_p['Time period'][j + 3*N*k] = f'{chunk}'
        df_p['Time period'][j + N + 3*N*k] = f'{chunk}'
        df_p['Time period'][j + 2*N + 3*N*k] = f'{chunk}'
        df_p['Strategy'][j + 3*N*k] = 'PhiID prediction'
        df_p['Strategy'][j + N + 3*N*k] = 'PhiID prediction'
        df_p['Strategy'][j + 2*N + 3*N*k] = 'PhiID prediction'
        
        df_p['Accuracy'][j + 3*N*k + 12*N] = guess_strength_super[j][0]
        df_p['Drowsiness'][j + 3*N*k + 12*N] = 'awake'
        df_p['Accuracy'][j + N + 3*N*k + 12*N] = guess_strength_super[j][1]
        df_p['Drowsiness'][j + N + 3*N*k + 12*N] = 'light drowsy'
        df_p['Accuracy'][j + 2*N + 3*N*k + 12*N] = guess_strength_super[j][2]
        df_p['Drowsiness'][j + 2*N + 3*N*k + 12*N] = 'heavy drowsy'
        df_p['Time period'][j + 3*N*k + 12*N] = f'{chunk}'
        df_p['Time period'][j + N + 3*N*k + 12*N] = f'{chunk}'
        df_p['Time period'][j + 2*N + 3*N*k + 12*N] = f'{chunk}'
        df_p['Strategy'][j + 3*N*k + 12*N] = 'Guessing'
        df_p['Strategy'][j + N + 3*N*k + 12*N] = 'Guessing'
        df_p['Strategy'][j + 2*N + 3*N*k + 12*N] = 'Guessing'
        
df_p.to_csv('LDA_p_values_syn.csv')
