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
# Load the dataset
df = pd.read_csv(f'perf_drow_data_cross_7580_xtx_pre2.csv')
df = df[df.performance != 'throwaway']

# Draw a categorical scatterplot to show each observation
#ax = sns.violinplot(x="drowsiness", y="metric", hue="performance", data=df, palette="muted", split=True).set(title = 'xtx(pretrial, electrode 80, electrode 75, experiment 1) split by performance and drowsiness', xlabel = 'drowsiness', ylabel = 'xtx')
ax = sns.swarmplot(data=df, x='metric', y='drowsiness', hue='performance',size = 3)