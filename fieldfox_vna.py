import pyvisa as visa
import numpy as np
import os
import csv

class SCPIInstrument:
    def __init__(self, visa_resource, timeout=10000):
        self.visa_resource = visa_resource
        self.visa_inst = visa.ResourceManager().open_resource(visa_resource)
        self.visa_inst.timeout = timeout

    def write(self, cmd):
        self.visa_inst.write(cmd)

    def query(self, command):
        return self.visa_inst.query(command)

    def read(self):
        return self.visa_inst.read()
    
    def read_raw(self):
        return self.visa_inst.read_raw()
    

class FieldFox(SCPIInstrument):
    def __init__(self, name, address):
        super().__init__(address)
        self.name = name

    # Measurement Configuration
    def set_mode(self, mode):
        self.write(f"INST '{mode}';*OPC?")
        return self.read()
    
    def set_measurement(self, param_number, param_name):
        self.write(f"CALC:PAR{param_number}:DEF {param_name}")

    def set_number_of_traces(self, count):
        self.write(f"CALCulate:PARameter:COUNt {count}")

    def select_trace(self, trace):
        self.write(f"CALC:PAR{trace}:SEL")
    
    def get_measurement(self):
        return self.query("CALCulate:PARameter:SELected:FORMat?")

    def set_trace_format(self, format_name):
        self.write(f"CALC:FORMat {format_name}")
        
    # Power Configuration
    def set_source_power(self, power_level):
        self.write(f"SOUR:POW {power_level}")

    def query_source_power(self):
        return self.query(":SOURce:POWer?")

    # Multi-trace Configurations
    def split_display_window(self, layout):
        self.write(f"DISPlay:WINDow:SPLit {layout}")

    def perform_measurement_conversion(self, func):
        self.write(f"CALCulate[:SELected]:CONVersion:FUNCtion {func}")

    # Sweep Settings
    def set_center_frequency(self, frequency):
        self.write(f"[:SENSe]:FREQuency:CENTer {frequency}")

    def set_frequency_span(self, span):
        self.write(f"[:SENSe]:FREQuency:SPAN {span}")

    def set_start_frequency(self, start_freq):
        self.write(f"FREQ:STAR {start_freq}")

    def set_stop_frequency(self, stop_freq):
        self.write(f"FREQ:STOP {stop_freq}")

    def read_x_axis_values(self):
        return self.query("[:SENSe]:FREQuency:DATA?")

    def set_resolution(self, num_points):
        self.write(f"SWE:POIN {num_points}")

    def set_sweep_time(self, sweep_time):
        self.write(f"[:SENSe]:SWEep:TIME {sweep_time}")

    def read_sweep_time(self):
        return self.query("[:SENSe]:SWEep:MTIMe?")

    def set_manual_source_power(self, power):
        self.write(f"SOURce:POWer {power}")

    def set_flat_source_power(self, power, mode="ON"):
        self.write(f"SOURce:POWer:ALC:MODE {mode};SOURce:POWer {power}")

    def set_trigger_source(self, source):
        self.write(f"TRIGger:SOURce {source}")

    def set_trigger_polarity(self, polarity):
        self.write(f"TRIGger:SLOPe {polarity}")

    # IFBW / Average / Smooth / Image Rej
    def set_if_bandwidth(self, bandwidth):
        self.write(f"[:SENSe]:BandWIDth {bandwidth}")

    def set_avg_number(self, avg_number):
        self.write(f"AVER:COUN {avg_number}")

    def clear_averaging(self):
        self.write("[:SENSe]:AVERage:CLEar")

    def set_averaging_mode(self, mode):
        self.write(f"[:SENSe]:AVERage:MODE {mode}")

    def set_smoothing_state(self, state):
        self.write(f"CALCulate[:SELected]:SMOothing[:STATe] {state}")

    def set_smoothing_aperture(self, aperture):
        self.write(f"CALCulate[:SELected]:SMOothing:APERture {aperture}")

    # Display Items
    def view_memory_trace_state(self):
        return self.query("DISPlay:WINDow:TRACe:MEMory:STATe?")

    def view_data_trace_state(self):
        return self.query("DISPlay:WINDow:TRACe:STATe?")

    def set_auto_scaling(self):
        self.write("DISPlay:WINDow:TRACe:Y:SCALe:AUTO")

    def set_scaling_bottom(self, bottom):
        self.write(f"DISPlay:WINDow:TRACe:Y:SCALe:BOTTom {bottom}")

    def set_scaling_per_division(self, division):
        self.write(f"DISPlay:WINDow:TRACe:Y:SCALe:PDIVision {division}")

    def set_scaling_reference_level(self, level):
        self.write(f"DISPlay:WINDow:TRACe:Y:SCALe:RLEVel {level}")

    def set_scaling_reference_position(self, position):
        self.write(f"DISPlay:WINDow:TRACe:Y:SCALe:RPOSition {position}")

    def set_scaling_top(self, top):
        self.write(f"DISPlay:WINDow:TRACe:Y:SCALe:TOP {top}")

    def set_electrical_delay(self, delay):
        self.write(f"CALCulate[:SELected]:CORRection:EDELay:TIME {delay}")

    def set_phase_offset(self, offset):
        self.write(f"CALCulate[:SELected]:CORRection:OFFSet:PHASe {offset}")

    def set_mag_offset(self, offset):
        self.write(f"CALCulate[:SELected]:OFFSet:MAGNitude {offset}")

    def set_mag_slope(self, slope):
        self.write(f"CALCulate[:SELected]:OFFSet:SLOPe {slope}")

    # Math
    def set_math_function(self, function):
        self.write(f"CALCulate[:SELected]:MATH:FUNCtion {function}")

    # Save / Recall Files - Data
    def save_data(self, file_dir, file_name):
        try:
            # Store the data on the FieldFox and then transfer it
            self.write(f"MMEM:STOR:FDAT '{file_name}'")
            self.write(f"MMEM:DATA? '{file_name}'")

            # Read the raw data from the instrument
            file_data = self.visa_inst.read_raw()

            # Save the file locally on your PC
            local_file_path = os.path.join(file_dir, file_name)
            with open(local_file_path, "wb") as fp:
                fp.write(file_data)

            print(f"Data saved successfully to {local_file_path}")
        
        except Exception as e:
            print(f"Error saving data: {e}")
            
            
    def save_snp_data(self, file_name):
        self.write(f"MMEMory:STORe:SNP '{file_name}'")

    def send_and_read_formatted_measured_data(self):
        return self.query("CALCulate[:SELected]:DATA:FDATa?")

    def send_and_read_formatted_memory_data(self):
        return self.query("CALCulate[:SELected]:DATA:FMEM?")

    def send_and_read_unformatted_measured_data(self):
        return self.query("CALCulate[:SELected]:DATA:SDATa?")

    def send_and_read_unformatted_memory_data(self):
        return self.query("CALCulate[:SELected]:DATA:SMEM?")

    def set_read_format(self, data_format):
        self.write(f"FORMat:{data_format}")

    
    def read_ins_settings (self, file_name, data_save_dir, ins_settings_save_dir):
        with open(os.path.join(data_save_dir, file_name), 'r') as csvfile:
            reader = csv.reader(csvfile)
    
        # Full path to the CSV file
        file_path = os.path.join(data_save_dir, file_name)

        # Read the first 31 lines
        with open(file_path, 'r') as csvfile:
            ins_settings_lines = [next(csvfile) for _ in range(30)]

        # Save the ins_settings_lines to a text file
        settings_file_path = os.path.join(ins_settings_save_dir, f"ins_settings_{file_name}.txt")
        with open(settings_file_path, 'w') as settings_file:
            settings_file.writelines(ins_settings_lines)

        return ins_settings_lines

    def read_csv_data(self, file_dir, file_path):
        with open(os.path.join(file_dir, file_path), 'r') as fp:
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
            
        return x_values, y_values    
    
    # Port Extensions
    def enable_port_extensions(self, state):
        self.write(f"[:SENSe]:CORRection:EXTension:STATe {state}")

    def set_port1_extension(self, extension_value):
        self.write(f"[:SENSe]:CORRection:EXTension:PORT1 {extension_value}")

    def set_port2_extension(self, extension_value):
        self.write(f"[:SENSe]:CORRection:EXTension:PORT2 {extension_value}")

    def set_velocity_factor(self, velocity_factor):
        self.write(f"[:SENSe]:CORRection:RVELocity:COAX {velocity_factor}")

    # Calibration
    def set_and_read_error_term_data(self, data):
        self.write(f"[:SENSe]:CORRection:COEFficient[:DATA] {data}")

    def read_number_of_cal_steps(self):
        return self.query("[:SENSe]:CORRection:COLLect:GUIDed:SCOunt?")

    def measure_step_number(self):
        return self.query("[:SENSe]:CORRection:COLLect:GUIDed:STEP:ACQuire?")

    def prompt_for_step_number(self):
        self.write("[:SENSe]:CORRection:COLLect:GUIDed:STEP:PROMpt")

    # ... (more calibration methods)

    # Time Domain (Opt 010)
    def enable_time_domain(self, state):
        self.write(f"CALCulate[:SELected]:TRANsform:TIME:STATe {state}")

    def set_time_domain_parameters(self, start, stop, center, span, type, stimulus, rtim, width, kbessel, lpfreq):
        self.write(f"CALCulate[:SELected]:TRANsform:TIME:STARt {start}")
        self.write(f"CALCulate[:SELected]:TRANsform:TIME:STOP {stop}")
        self.write(f"CALCulate[:SELected]:TRANsform:TIME:CENTer {center}")
        self.write(f"CALCulate[:SELected]:TRANsform:TIME:SPAN {span}")
        self.write(f"CALCulate[:SELected]:TRANsform:TIME:{type} {stimulus}")
        self.write(f"CALCulate[:SELected]:TRANsform:TIME:STEP:RTIMe {rtim}")
        self.write(f"CALCulate[:SELected]:TRANsform:TIME:IMPulse:WIDTh {width}")
        self.write(f"CALCulate[:SELected]:TRANsform:TIME:KBESsel {kbessel}")
        self.write(f"CALCulate[:SELected]:TRANsform:TIME:LPFREQuency {lpfreq}")

    # Time Domain Gating
    def enable_time_domain_gating(self, state):
        self.write(f"CALCulate[:SELected]:FILTer[:GATE]:TIME:STATe {state}")

    def set_time_domain_gating_parameters(self, start, stop, center, span, shape):
        self.write(f"CALCulate[:SELected]:FILTer[:GATE]:TIME:STARt {start}")
        self.write(f"CALCulate[:SELected]:FILTer[:GATE]:TIME:STOP {stop}")
        self.write(f"CALCulate[:SELected]:FILTer[:GATE]:TIME:CENTer {center}")
        self.write(f"CALCulate[:SELected]:FILTer[:GATE]:TIME:SPAN {span}")
        self.write(f"CALCulate[:SELected]:FILTer[:GATE]:TIME:SHAPe {shape}")
        
