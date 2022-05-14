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
df_p = pd.DataFrame(columns = ['Weight vectors', 'Accuracy', 'Strategy' , 'Time period', 'Drowsiness'], index=range(N*24))
for k in range(0,4):
    chunk = chunks[k]
    predictive_strength_super = [None]*N
    guess_strength_super = [None]*N
    weight_vectors_super = [None]*N
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
        for i in range(0,2):
            drowsy_level = drowsy_levels[i]
            data_forLDA = data[data['drowsiness'] == f'{drowsy_level}']   
            data_forLDA = data_forLDA.reset_index(drop=True)
            x = np.transpose([data_forLDA['rtr'], data_forLDA['rtx'], data_forLDA['rty'], data_forLDA['rts'], 
            data_forLDA['xtr'], data_forLDA['xtx'], data_forLDA['xty'], data_forLDA['xts'], 
            data_forLDA['rtr'], data_forLDA['rtx'], data_forLDA['yty'], data_forLDA['yts'],
            data_forLDA['str'], data_forLDA['stx'], data_forLDA['sty'], data_forLDA['sts']])
            y = data_forLDA['performance'].replace({'hit': 1, 'miss': 0})
            #take 80% of trials to train with and 20% of trials to predict with
            learning_trials = random.sample(range(1, len(y)), math.floor(0.8*len(y)))
            predicting_trials =  list(set(range(1, len(y))) - set(learning_trials))
            learning_x = [x[j] for j in learning_trials]
            learning_y = [y[j] for j in learning_trials]
            predicting_x = [x[j] for j in predicting_trials]
            predicting_y = [y[j] for j in predicting_trials]
            clf = LinearDiscriminantAnalysis(solver = 'lsqr', shrinkage = 1)
            clf.fit(learning_x, learning_y)
            metrics[i]['predicted_value'] = clf.predict(predicting_x)
            metrics[i]['actual_value'] = predicting_y
            metrics[i]['drowsiness'] = metrics[i]['drowsiness'].fillna(f'{drowsy_level}')
            metric = pd.concat([metric, metrics[i]])
            truth_tables[i] = pd.crosstab(metrics[i]['predicted_value'], metrics[i]['actual_value'])
            #sometimes the prediction will contain no predicted negatives or positives, so we have to catch keyerror exceptions
            try:
                predictive_strength[i] = (truth_tables[i].loc[0, 0] + truth_tables[i].loc[1, 1])/len(predicting_y)
            except:
                try:
                    predictive_strength[i] = (truth_tables[i].loc[0, 0])/len(predicting_y)
                except:
                    predictive_strength[i] = (truth_tables[i].loc[1, 1])/len(predicting_y)
            p1 = learning_y.count(1)/len(learning_y)
            p2 = predicting_y.count(1)/len(predicting_y)
            guess_strength[i] = p1*p2 + (1-p1)*(1-p2)
            #find the normalized weight_vectors, which represent how important each atom is to the LDA prediction
            weight_vectors[i] = np.divide(clf.coef_, np.mean(x, axis=0))
        predictive_strength_super[j] = predictive_strength.copy()
        guess_strength_super[j] = guess_strength.copy()
        weight_vectors_super[j] = weight_vectors.copy()
    
    for j in range(0, N):
        df_p['Accuracy'][j + 3*N*k] = predictive_strength_super[j][0]
        df_p['Weight vectors'][j + 3*N*k] = weight_vectors_super[j][0]
        df_p['Drowsiness'][j + 3*N*k] = 'awake'
        df_p['Accuracy'][j + N + 3*N*k] = predictive_strength_super[j][1]
        df_p['Drowsiness'][j + N + 3*N*k] = 'light drowsy'
        df_p['Weight vectors'][j + N + 3*N*k] = weight_vectors_super[j][1]
        df_p['Accuracy'][j + 2*N + 3*N*k] = predictive_strength_super[j][2]
        df_p['Drowsiness'][j + 2*N + 3*N*k] = 'heavy drowsy'
        df_p['Weight vectors'][j + 2*N + 3*N*k] = weight_vectors_super[j][2]
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
        
df_p.to_csv('LDA_p_values_reg.csv')
