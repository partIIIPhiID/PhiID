# -*- coding: utf-8 -*-
"""
Created on Wed May 11 09:31:47 2022

@author: andre
"""

import random
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LogNorm

df = pd.read_csv('weight_vectors_absmean_heatmap.csv')
#a = df[df.drowsiness == 'alert']
a = df[df.drowsiness == 'light drowsy']
a = a.drop(columns = 'drowsiness')
a = a.pivot(index = "atom", columns = "time period", values = "weight vector")
a['stimulus'] = np.NaN
a = a.reindex(["xtx", 'yty', "rtr", "sts", 'xty', 'ytx', 'rtx', 'rty', 'xtr', 'ytr', 'rts', 'xts', 'yts', 'str', 'stx', 'sty'])
a = a[['pre1', 'pre2', 'stimulus', 'post1', 'post2']]
a = a.rename(columns={"pre1": "(-4,-2)", "pre2": "(-2,0)", 'post1': '(2,4)', 'post2': '(4,6)'})
ax = sns.heatmap(data = a, cmap = 'coolwarm', annot = False, vmin= -500, vmax = 500).set(xlabel = 'time period /s')


#a = a.drop(columns = 'drowsiness')
#a = a.pivot(index = "atom", columns = "time period", values = "weight vector")
#ax = sns.heatmap(data = a, cmap = 'coolwarm', annot = False, vmin=-500, vmax=500)