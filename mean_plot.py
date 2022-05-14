# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 21:58:12 2022

@author: andre
"""



import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy

sns.set_theme(style="whitegrid", palette="muted")
data=[]
drowsy_levels = ['awake', 'light drowsy', 'heavy drowsy']
atoms = ["rtr", "sts"]
chunks = ["pre1", "pre2", "post1", "post2"]
distances = ["neighbours", "close range", "long range"]
electrode_locations = pd.read_csv('electrode_locations.csv')
elec_list = pd.read_csv('rand_electrode_list.csv')
participant_number = pd.read_csv('participant_number.csv')
N = 500
min_length = 64
max_length = 169
data = pd.DataFrame(columns = ['mean', 'std', 'electrode A', 'electrode B', 'drowsiness', 'seperation', 'chunk', 'atom'])
for atom in atoms:
    for chunk in chunks:
        for drowsy_level in drowsy_levels:
            for n_i in range(0,499):
                try:
                    elecA = int(elec_list.loc[n_i].at['electrode A'])
                    elecB = int(elec_list.loc[n_i].at['electrode B'])
                    df = pd.read_csv(f'performance_data_cross_{elecA}{elecB}_{atom}_{chunk}.csv')
                    df = df[df.performance != 'throwaway']
                    mean = np.mean(df['metric'])
                    std = np.std(df['metric'])
                    seperation = ((electrode_locations.loc[elecA].at["x"] - electrode_locations.loc[elecB].at["x"])**2 +
                                  (electrode_locations.loc[elecA].at["y"] - electrode_locations.loc[elecB].at["y"])**2 +
                                  (electrode_locations.loc[elecA].at["z"] - electrode_locations.loc[elecB].at["z"])**2)
                    if seperation < min_length:
                        distance = distances[0]
                    elif seperation > max_length:
                        distance = distances[2]
                    else:
                        distance = distances[1]
                    
                except:
                    print(f'missing data for {n_i}')
                #print(difference)
                #print(std)
                
                data.append([mean, std, f'{elecA}', f'{elecB}', f'{drowsy_level}', f'{distance}', f'{chunk}',f'{atom}'])
        
        analysis = pd.DataFrame(data.loc[(data['drowsiness'] == f'{drowsy_level}') & (df['performance'] == 'hit')], columns = ['mean', 'std', 'electrode A', 'electrode B', 'drowsiness', 'seperation'])
        df['drowsiness'] = df.drowsiness.astype('category')
        #print(analysis)
        analysis.to_csv('out.csv')
        ax = sns.swarmplot(data=analysis, x='mean', y = 'drowsiness', hue = 'seperation', palette = 'tab10', size = 1.4, hue_order = ["neighbours", "close range", "long range"], dodge = True).set(title = f'{atom} mean at {chunk}', ylabel = 'drowsiness', xlabel = f'mean {atom} value')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.savefig(f'mean_{atom}_{chunk}_crosselec_crosspart_exp1.png', dpi=300, bbox_inches = "tight")
        plt.clf()
        data = []