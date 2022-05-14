# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 16:07:19 2022

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
participant_list = pd.read_csv('participant_number.csv')
N = 500
min_length = 64
max_length = 169
data = pd.DataFrame(columns = ['difference', 'normalized difference', 'std', '-log(p)', 'electrode A', 'electrode B', 'drowsiness', 'seperation', 'chunk', 'atom', 'participant'])
for atom in atoms:
    for chunk in chunks:
        for drowsy_level in drowsy_levels:
            for n_i in range(0,499):
                try:
                    elecA = int(elec_list.loc[n_i].at['electrode A'])
                    elecB = int(elec_list.loc[n_i].at['electrode B'])
                    df = pd.read_csv(f'performance_data_cross_{elecA}{elecB}_{atom}_{chunk}.csv')
                    df['participant'] = participant_list
                    for participant_number in range(1,31):
                        df2 = df[(df.performance != 'throwaway') & (df.participant == participant_number) & (df['drowsiness'] == f'{drowsy_level}')]
                        df_hits = df2.loc[(df2['performance'] == 'hit')]
                        df_misses = df2.loc[(df2['performance'] == 'miss')]
                        difference = (np.mean(df_hits)['metric'] - np.mean(df_misses)['metric'])
                        norm_difference = difference/np.mean(df.loc[(df['drowsiness'] == f'{drowsy_level}')])[0]
                        std_hits = np.std(df_hits['metric'])/(len(df_hits)-1)
                        std_misses = np.std((df_misses)['metric'])/(len(df_misses)-1)
                        std = np.sqrt(std_hits**2 + std_misses**2)
                        stat_test = -np.log10(scipy.stats.ttest_ind(df_hits['metric'],df_misses['metric'])[1])
                        seperation = ((electrode_locations.loc[elecA].at["x"] - electrode_locations.loc[elecB].at["x"])**2 +
                                      (electrode_locations.loc[elecA].at["y"] - electrode_locations.loc[elecB].at["y"])**2 +
                                      (electrode_locations.loc[elecA].at["z"] - electrode_locations.loc[elecB].at["z"])**2)
                        if seperation < min_length:
                            distance = distances[0]
                        elif seperation > max_length:
                            distance = distances[2]
                        else:
                            distance = distances[1]
                        temp_data = pd.DataFrame([[difference, norm_difference, std, stat_test, f'{elecA}', f'{elecB}', f'{drowsy_level}', f'{distance}', f'{chunk}',f'{atom}', participant_number]], columns = ['difference', 'normalized difference', 'std', '-log(p)', 'electrode A', 'electrode B', 'drowsiness', 'seperation', 'chunk', 'atom', 'participant'])
                        data = pd.concat([data, temp_data])
                        
                except:
                    pass
                #print(difference)
                #print(std)

        print(f"outputting for {atom} at {chunk}")
        #analysis = pd.DataFrame(data.loc[(data['atom'] == f'{atom}') & (data['chunk'] == f'{chunk}')], columns = ['difference','normalized difference', 'std', '-log(p)', 'electrode A', 'electrode B', 'drowsiness', 'seperation', 'chunk', 'atom', 'participant'])
        #df['drowsiness'] = df.drowsiness.astype('category')
        #analysis.to_csv('out.csv')
        #ax = sns.swarmplot(data=analysis, x='difference', y = 'drowsiness', hue = 'participant', size = 1.4, dodge = True).set(title = f'{atom} performance difference at {chunk}', ylabel = 'drowsiness', xlabel = 'difference')
        #ax = sns.violinplot(data=analysis, x='difference', y = 'participant').set(title = f'{atom} performance difference at {chunk}', ylabel = 'drowsiness', xlabel = 'difference')
        #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        #plt.savefig(f'betweenparticipants/difference/performance_{atom}_{chunk}_crosselec_crosspart_exp1.png', dpi=300, bbox_inches = "tight")
        #plt.clf()
data.to_csv('betweenparticipants/final_data_betweenparticipant.csv')
print('finished!')