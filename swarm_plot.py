# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 14:31:23 2022

@author: andre
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", palette="muted")

# Load the dataset
df = pd.read_csv('fulldataset2.csv')

# Draw a categorical scatterplot to show each observation
ax = sns.swarmplot(data=df, x='atomvalue', y='chunks', hue='response',size = 2 )
ax.set(ylabel='time chunk')
ax.set(xlabel='rtr atom value')
