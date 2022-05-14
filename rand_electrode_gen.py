# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 16:05:12 2022

@author: andre
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy
import random
import math

N = 92
N_sample = 500
x = random.sample(range(N**2), N_sample)
electrode_a = np.zeros(N_sample)
electrode_b = np.zeros(N_sample)
for i in range(0,N_sample):
  electrode_a[i] = math.floor(x[i]/N)
  electrode_b[i] = x[i]%N

df = pd.DataFrame(np.transpose([electrode_a, electrode_b]), columns = ['electrode A','electrode B' ])
df.to_csv('rand_electrode_list.csv')
print(electrode_a)
print(electrode_b)