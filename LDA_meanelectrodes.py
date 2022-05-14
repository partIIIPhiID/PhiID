# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 12:22:18 2022

@author: andre
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import sys

df = pd.read_csv(f'performance_data_cross_2769_sts_pre2.csv')
sys.exit("quit")
sns.set_theme(style="whitegrid", palette="muted")
data=[]
drowsy_levels = ['awake', 'light drowsy', 'heavy drowsy']
atoms = ["rtr", "rtx", "rty", "rts", "str", "stx", "sty", "sts", "xtr", "xtx", "xty", "xts", "ytr", "ytx","yty", "yts"]
chunks = ["pre1", "pre2", "post1", "post2"]
distances = ["neighbours", "close range", "long range"]
electrode_locations = pd.read_csv('electrode_locations.csv')
elec_list = pd.read_csv('rand_electrode_list.csv')
participant_number = pd.read_csv('participant_number.csv')
N = 500
min_length = 64
max_length = 169
data = pd.DataFrame(columns = ['normalized difference', 'std', '-log(p)', 'electrode A', 'electrode B', 'drowsiness', 'seperation', 'chunk', 'atom'])
for atom in atoms:
    for chunk in chunks:
        for drowsy_level in drowsy_levels:
            for n_i in range(0,499):
                try:
                    elecA = int(elec_list.loc[n_i].at['electrode A'])
                    elecB = int(elec_list.loc[n_i].at['electrode B'])
                    df = pd.read_csv(f'performance_data_cross_{elecA}{elecB}_{atom}_{chunk}.csv')
                    df = df[df.performance != 'throwaway']
                    #length = df.size 
                    for i in range:
                            metric_sum[i]['atom'] = df[i]#this should be an nx16 matrix containing the sum of each PhiID atom at each trial  
                except:
                    print(f'missing data for {n_i}')