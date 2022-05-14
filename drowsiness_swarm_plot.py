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

# Load the dataset
df = pd.read_csv('testdata_withdrowsiness_5_sts_pre2.csv')
df = df[df.performance != 'throwaway']

# Draw a categorical scatterplot to show each observation
ax = sns.violinplot(x="drowsiness", y="metric", hue="performance", data=df, palette="muted", split=True)
#ax = sns.swarmplot(data=df, x='metric', y='drowsiness', hue='performance',size = 3)
ax.set(xlabel='drowsiness level')
ax.set(ylabel='atom value')