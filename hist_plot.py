# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 16:47:16 2022

@author: andre
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy

sns.set_theme(style="whitegrid", palette="muted")

# Load the dataset
df = pd.read_csv('fulldataset2_07.csv')
df = df[0:518] #trim the data frame to only include the first time chunk
# Draw a categorical scatterplot to show each observation
ax = sns.histplot(data=df, x='atomvalue', hue = 'response', stat = 'density', multiple = 'fill', common_norm = 'false')
ax.set(ylabel='probability')
ax.set(xlabel='pretrial rtr atom value')
