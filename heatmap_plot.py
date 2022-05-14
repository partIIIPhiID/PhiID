# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 16:09:18 2022

@author: andre
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy

sns.set_theme(style="whitegrid", palette="muted")

# Load the dataset
#atoms = ["rtr", "rtx", "rty", "rts", "str", "stx", "sty", "sts", "xtr", "xtx", "xty", "xts", "ytr", "ytx","yty", "yts"]
#chunks = ["pre1", "pre2", "post1", "post2"]
#atoms = ["rtr", "sts"]
#chunks = ["pre1", "pre2", "post1", "post2"]
#for x in atoms:
    #for y in chunks:
atom = 'rtr'
chunk = 'pre2'
test = 'difference3'
df = pd.read_csv(f'csv_for_heatmap_6580_{atom}{chunk}.csv')
df.columns = ['electrode A', 'electrode B', 'difference', 'difference2', 'difference3', 'std', 't-test' ]
df.replace(0, np.nan, inplace=True)
df['t-test'] = -np.log(df['t-test'])
df1 = df.pivot("electrode A", "electrode B", f'{test}')
# Draw a categorical scatterplot to show each observation
if test == 'difference':
    ax= sns.heatmap(df1, cmap = 'coolwarm', vmin=-0.03, vmax=0.03).set(title = f'{test} for {atom}(pre-trial 2, electrode A, electrode B)')
if test == 't-test':
    ax= sns.heatmap(df1, vmin=0, vmax=3, cmap = 'rocket_r', cbar_kws={'label': '-log(p)'}).set(title = f'{test} for {atom}(pre-trial 2, electrode A, electrode B)')
if test == 'difference2':
    ax= sns.heatmap(df1, cmap = 'coolwarm', vmin=-3, vmax=3).set(title = f'{test} for {atom}({chunk}, electrode A, electrode B, experiment 1)')
if test == 'difference3':
    ax= sns.heatmap(df1, cmap = 'coolwarm', vmin=-0.5, vmax=0.5).set(title = f'{test} for {atom}({chunk}, electrode A, electrode B, experiment 1)')
plt.savefig(f'{atom}_{chunk}_{test}_heatmapplot_exp1.png')