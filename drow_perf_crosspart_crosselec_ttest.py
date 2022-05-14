# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 10:33:00 2022

@author: andre
"""


import numpy as np
import scipy.stats
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", palette="muted")
data=[]
drowsy_levels = ['awake', 'light drowsy', 'heavy drowsy']
for drowsy_level in drowsy_levels:
    for elecA in range(65,80):
        for elecB in range(elecA + 1, 80):
            df = pd.read_csv(f'performance_data_cross_{elecA}{elecB}_rtr_pre2.csv')
            df = df[df.performance != 'throwaway']
            df_hits = df.loc[(df['drowsiness'] == f'{drowsy_level}') & (df['performance'] == 'hit')]
            df_misses = df.loc[(df['drowsiness'] == f'{drowsy_level}') & (df['performance'] == 'miss')]
            difference = np.mean(df_hits['metric']) - np.mean(df_misses['metric'])
            std_hits = np.std(df_hits['metric'])/(len(df_hits)-1)
            std_misses = np.std((df_misses)['metric'])/(len(df_misses)-1)
            std = np.sqrt(std_hits**2 + std_misses**2)
            ttest = scipy.stats.ttest_ind(df_hits['metric'], df_misses['metric'])[0]
            ttest_p = scipy.stats.ttest_ind(df_hits['metric'], df_misses['metric'])[1]
            #print(difference)
            #print(difference)
            #print(std)
            data.append([difference, std, ttest, ttest_p, f'{elecA}', f'{elecB}', f'{drowsy_level}'])

analysis = pd.DataFrame(data, columns = ['difference', 'std', 't-test','t-test_p', 'electrode A', 'electrode B', 'drowsiness'])
df['drowsiness'] = df.drowsiness.astype('category')
#print(analysis)
analysis.to_csv('out.csv')
ax = sns.swarmplot(data=analysis, x='difference', y = 'drowsiness', palette = 'viridis', size = 3)
# Now connect the dots
# Find idx0 and idx1 by inspecting the elements return from ax.get_children()
# ... or find a way to automate it
idx0 = 0
idx1 = 1
locs1 = ax.get_children()[idx0].get_offsets()
locs2 = ax.get_children()[idx1].get_offsets()

# before plotting, we need to sort so that the data points
# correspond to each other as they did in "set1" and "set2"
sort_idxs1 = np.argsort(df['drowsiness'] == 'awake')
sort_idxs2 = np.argsort(df['drowsiness'] == 'light drowsy')

# revert "ascending sort" through sort_idxs2.argsort(),
# and then sort into order corresponding with set1
locs2_sorted = locs2[sort_idxs2.argsort()][sort_idxs1]

for i in range(locs1.shape[0]):
    x = [locs1[i, 0], locs2_sorted[i, 0]]
    y = [locs1[i, 1], locs2_sorted[i, 1]]
    ax.plot(x, y, color="black", alpha=0.1)
#ax = sns.scatterplot(data = analysis, x="t-test", y="t-test_p", hue = 'drowsiness')
# Draw a categorical scatterplot to show each observation
#ax = sns.violinplot(x="drowsiness", y="metric", hue="performance", data=df, palette="muted", split=True).set(title = 'xtx(pretrial, electrode 80, electrode 75, experiment 1) split by performance and drowsiness', xlabel = 'drowsiness', ylabel = 'xtx')
#ax = sns.swarmplot(data=df, x='metric', y='drowsiness', hue='performance',size = 3)