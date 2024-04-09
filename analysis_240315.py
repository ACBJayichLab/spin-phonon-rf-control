# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:44:35 2024

@author: lab
"""

import time
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(r'G:\My Drive\Postdoc Work\many body physics\code\analysis\helper')

import plot_data
import numpy as np
import csv
from datetime import datetime
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

# Function to load CSV files and extract X and Y data
def load_csv_files(files):
    data_arrays = []
    for file in files:
        df = pd.read_csv(file)
        X = df['X'].values
        Y = df['Y'].values
        data_arrays.append((X, Y))
    return data_arrays

# Get list of CSV files in the current directory
csv_files = glob.glob('onlydata*.csv')

# Load CSV files and extract X, Y data
data = load_csv_files(csv_files)

# Plot X against Y for each file
plt.figure(figsize=(10, 6))
for X, Y in data:
    plt.plot(X, Y, label="Data")
plt.xlabel('X')
plt.ylabel('Y')
plt.title('X vs Y')
plt.legend()
plt.grid(True)
plt.show()