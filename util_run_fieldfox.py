from fieldfox_vna import FieldFox
import os
import matplotlib.pyplot as plt
from datetime import datetime
import time

# Save the plot with a timestamp in the filename
timestamp = str(datetime.now().strftime("%y%m%d"))


inst_name = "MyFieldFox"
inst_addr = "TCPIP0::192.168.1.135::inst0::INSTR"  # Replace with your instrument's VISA address

trace_number = 1
measurement = "S11"
power = -45 # dBm
freq_start = 2.5e9 # Hz
freq_stop = 3.0e9 # Hz
num_points = 601
avg_number = 50
wait_time = 10 # seconds




file_dir = './Data'
file_name = timestamp + '_cable 2_'+str(power)+'.csv'
file_path = os.path.join(file_dir, file_name)


# Set up the FieldFox VNA
ff = FieldFox(inst_name, inst_addr)
ff.set_mode("NA")
ff.set_measurement(trace_number, measurement)
ff.set_trace_format("MLOGarithmic")
ff.set_start_frequency(freq_start)
ff.set_stop_frequency(freq_stop)
ff.set_resolution(num_points)
ff.set_source_power(power)
power_read = float(ff.query("SOURce:POWer?"))
print(f"Power level: {power_read:.2f} dBm")
ff.set_avg_number(avg_number)

# Wait for the measurement to complete
time.sleep(wait_time)

# Save the data to a CSV file
ff.save_data(file_dir, file_name)
xdata, ydata = ff.read_csv_data(file_dir, file_name)

ff.set_source_power(-45)


# Plot
fig, ax = plt.subplots()
ax.plot(xdata/1e9, ydata)
ax.set_xlabel("Frequency (GHz)")
ax.set_ylabel("Magnitude (dB)")
ax.set_title(f"VNA Measurement: {measurement}\n{file_path}")
plt.show()
