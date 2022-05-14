# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 00:28:12 2022

@author: andre
"""

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
ax = sns.violinplot(data=df, x='atomvalue', y='chunks',size = 2 )
ax.set(ylabel='response')
ax.set(xlabel='rtr atom value')
