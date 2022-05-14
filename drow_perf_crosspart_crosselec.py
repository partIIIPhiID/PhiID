# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 10:33:00 2022

@author: andre
"""


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", palette="muted")
data=[]
drowsy_levels = ['awake', 'light drowsy', 'heavy drowsy']
atoms = ["rtr", "rtx", "rty", "rts", "str", "stx", "sty", "sts", "xtr", "xtx", "xty", "xts", "ytr", "ytx","yty", "yts"]
chunks = ["pre1", "pre2", "post1", "post2"]
for atom in atoms:
    for chunk in chunks:
        for drowsy_level in drowsy_levels:
            for elecA in range(65,80):
                for elecB in range(elecA + 1, 80):
                    df = pd.read_csv(f'performance_data_cross_{elecA}{elecB}_{atom}_{chunk}.csv')
                    df = df[df.performance != 'throwaway']
                    df_hits = df.loc[(df['drowsiness'] == f'{drowsy_level}') & (df['performance'] == 'hit')]
                    df_misses = df.loc[(df['drowsiness'] == f'{drowsy_level}') & (df['performance'] == 'miss')]
                    difference = np.mean(df_hits)['metric'] - np.mean(df_misses)['metric']
                    std_hits = np.std(df_hits['metric'])/(len(df_hits)-1)
                    std_misses = np.std((df_misses)['metric'])/(len(df_misses)-1)
                    std = np.sqrt(std_hits**2 + std_misses**2)
                    #print(difference)
                    #print(std)
                    data.append([difference, std, f'{elecA}', f'{elecB}', f'{drowsy_level}'])
        
        analysis = pd.DataFrame(data, columns = ['difference', 'std', 'electrode A', 'electrode B', 'drowsiness'])
        df['drowsiness'] = df.drowsiness.astype('category')
        #print(analysis)
        analysis.to_csv('out.csv')
        ax = sns.violinplot(data=analysis, x='difference', y = 'drowsiness', palette = 'viridis', size = 3).set(title = f'{atom} performance difference seperated by drowsiness', ylabel = 'drowsiness', xlabel = f'{atom} difference at {chunk}', xlim=(-0.15, 0.15))
        plt.savefig(f'perf_drow_{atom}_{chunk}_crosselec_crosspart_exp1.png', dpi=300, bbox_inches = "tight")
        plt.clf()
        # Draw a categorical scatterplot to show each observation
        #ax = sns.violinplot(x="drowsiness", y="metric", hue="performance", data=df, palette="muted", split=True).set(title = 'xtx(pretrial, electrode 80, electrode 75, experiment 1) split by performance and drowsiness', xlabel = 'drowsiness', ylabel = 'xtx')
        #ax = sns.swarmplot(data=df, x='metric', y='drowsiness', hue='performance',size = 3)