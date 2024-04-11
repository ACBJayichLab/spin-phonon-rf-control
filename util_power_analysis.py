import matplotlib.pyplot as plt
import csv
import os
import numpy as np

file_dir = './Data'
file_header = "240411_cable 2_"
power_lst = [-20, -25, -30, -35, -40, -45]

fig, ax = plt.subplots()
ax.set_xlabel("Frequency (GHz)")
ax.set_ylabel("Magnitude (dB)")
ax.set_title("VNA Measurement: S22")

for power in power_lst:
    file_name = file_header + str(power) + '.csv'

    with open(os.path.join(file_dir, file_name), 'r') as fp:
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
        
        ax.plot(x_values, y_values, label = f"{power} dBm")
    
fig.legend()
plt.show()
