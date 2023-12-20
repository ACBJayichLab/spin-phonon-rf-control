# Spin-Phonon RF Control

## Overview

Spin-Phonon RF Control is a Python package designed for instrument control and data analysis in spin-phonon experiments. It provides a set of tools for interacting with RF instruments, extracting data from CSV files, and plotting experimental results.

## Installation

Clone the repository and install the required dependencies.

```bash
git clone https://github.com/your-username/spinphonon-rfcontrol.git
cd spinphonon-rfcontrol
pip install -r requirements.txt

Features
visainstrument.py
VisaInstrument Class
The VisaInstrument class provides a generic interface for communicating with RF instruments using the VISA protocol. It includes methods for sending commands, reading responses, and saving instrument settings and data.

Methods:
send_command(command: str): Sends a command to the instrument.
read_raw() -> bytes: Reads raw data from the instrument.
Usage:
python
Copy code
# Example usage of VisaInstrument
fieldfox = VisaInstrument('TCPIP0::192.168.1.100::inst0::INSTR')
fieldfox.send_command('*IDN?')
response = fieldfox.read_raw()
print(response)
create_instruments.py
FieldFox Class
The FieldFox class extends the VisaInstrument class and provides additional methods for specific operations related to the Keysight FieldFox RF analyzer. It includes methods for plotting and saving CSV data, as well as saving traces to CSV files.

Methods:
plot_and_save_csv_data(file_name: str, data_save_dir: str, ins_settings_save_dir: str, fig_save_dir: str, plot_title: str, pres_type='paper'): Plots and saves CSV data, along with instrument settings.
save_data_trace_to_csv(file_name: str, save_path: str): Saves a data trace to a CSV file.
Usage:
python
Copy code
# Example usage of FieldFox class
fieldfox = FieldFox('TCPIP0::192.168.1.100::inst0::INSTR')
fieldfox.plot_and_save_csv_data('experiment_data.csv', 'data_folder', 'settings_folder', 'figures_folder', 'Experiment Plot')
Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
Jayameenakshi Venkatraman
jayavenkat@ucsb.edu
