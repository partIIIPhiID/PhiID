# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 11:23:09 2022

@author: andre
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", palette="muted")
for i in range(1,60):
    try:
        # Load the dataset
        df = pd.read_csv(f'perf_drow_data_{i}_sts_pre2.csv')
        df = df[df.performance != 'throwaway']
        
        # Draw a categorical scatterplot to show each observation
        ax = sns.violinplot(x="drowsiness", y="metric", hue="performance", data=df, palette="muted", split=True)
        #ax = sns.swarmplot(data=df, x='metric', y='drowsiness', hue='performance',size = 3)
        ax.set(xlabel='drowsiness level')
        ax.set(ylabel='atom value')
        plt.savefig(f'violin_rtr_{i}_heatmapplot_exp1.png')
        plt.clf()
    except Exception as e:
        print(e)
        