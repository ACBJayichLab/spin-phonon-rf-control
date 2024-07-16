import matplotlib.pyplot as plt
import csv
import os
import numpy as np

file_dir = './Data/240418'
# file_header = "240411_cable 2_"
# power_lst = [-20, -25, -30, -35, -40, -45]
file2 = "240418_150537_whole cables without device_S11.csv"
file1 = "240418_134108_whole cables with device_S11.csv"



fig, ax = plt.subplots()
ax.set_xlabel("Frequency (GHz)")
ax.set_ylabel("Magnitude (dB)")
ax.set_title("VNA Measurement: S11")

with open(os.path.join(file_dir, file1), 'r') as fp:
    reader = csv.reader(fp)

    # Skip the first 31 lines
    for _ in range(31):
        next(reader)

    # Read the data until the "END" line
    data_rows = []
    x_values = []
    y_values = []
    
    for row in reader:
        if row and row[0].strip().upper() == "END":
            break
        data_rows.append(row)
        x_values.append(float(row[0]))
        y_values.append(float(row[1]))

    x_values = np.asarray(x_values)
    y_values = np.asarray(y_values)

with open(os.path.join(file_dir, file2), 'r') as fp:
    reader = csv.reader(fp)

    # Skip the first 31 lines
    for _ in range(31):
        next(reader)

    # Read the data until the "END" line
    data_rows2 = []
    x_values2 = []
    y_values2 = []
    
    for row in reader:
        if row and row[0].strip().upper() == "END":
            break
        data_rows2.append(row)
        x_values2.append(float(row[0]))
        y_values2.append(float(row[1]))

    x_values2 = np.asarray(x_values2)
    y_values2 = np.asarray(y_values2)
 


ax.plot(x_values, y_values)
ax.plot(x_values2, y_values2)
ax.plot(x_values, y_values-y_values2)
    
fig.legend()
plt.show()
