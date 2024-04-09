#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 13:43:38 2023

@author: jaya
"""


from visainstrument import FieldFox
import matplotlib.pyplot as plt
from datetime import datetime
ins_settings_save_dir = r'G:/My Drive/Postdoc Work/spin-phonon/experiment/ins_settings/'
data_save_dir = r'G:/My Drive/Postdoc Work/spin-phonon/experiment/data/'
fig_save_dir = r'G:/My Drive/Postdoc Work/spin-phonon/experiment/images/vna_images/'
file_name = r'dataexample.csv'

# Save the plot with a timestamp in the filename
timestamp = 'data'+str(datetime.now().strftime("%Y%m%d"+'_'+"%H%M%S"))
file_name = timestamp + '.csv'

def format_e(n):
    # coverts to scientific notation, convenient for file saving
    a = '%E' % n
    return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]
#%%
if 1:
    trace_number = 1
    measurement_format = 'S11'
    power = -45 #dBm
    freq_start = 1e9 #Hz
    freq_stop = 10e9 #Hz
    if_bandwidth = 1e3 #1Hz
    instrument_name = "MyFieldFox"
    instrument_address = "TCPIP0::192.168.1.135::inst0::INSTR"  # Replace with your instrument's VISA address
    num_points = 1601
    power_level = -40
    
    fieldfox = FieldFox(instrument_name, instrument_address)

    # # Example usage
   #%%
    fieldfox.set_number_of_traces(1)
    fieldfox.set_measurement(1)
    fieldfox.create_measurement(1, measurement_format)
    fieldfox.set_trace_format("MLOG")
    # fieldfox.split_display_window("D1")[]
    # fieldfox.set_start_frequency(freq_start)
    # fieldfox.set_stop_frequency(freq_stop)
    # fieldfox.perform_measurement_conversion("DBM")
    # fieldfox.set_resolution(num_points)
    # # Set the power level to 0 dBm (adjust the value as needed)
    # fieldfox.set_source_power(f"SOURce:POWer {power_level} dBm")

    # # Query the power level to verify the setting
    result = fieldfox.query("SOURce:POWer?")
    # # print(result)
    
    # # Generate plot title
    plot_title = f"{measurement_format}_Power{power}"#"_Freq{format_e(freq_start)}_{format_e(freq_stop)}_IFBW{format_e(if_bandwidth)}"
    
    # print (plot_title)
     #%%
    print(f"Power Level Set: {result} dBm")
    
    fieldfox.save_data_trace_to_csv(str(file_name),data_save_dir)#r str(file_name)+'.csv')#(r'G:\My Drive\Postdoc Work\spin-phonon\experiment\data\' + str(file_name))
    fieldfox.set_delay(10)
    fieldfox.plot_data(file_name, data_save_dir, \
                                ins_settings_save_dir, fig_save_dir, \
                                    plot_title, pres_type='paper')