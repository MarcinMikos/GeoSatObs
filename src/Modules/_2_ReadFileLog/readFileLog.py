# Libraries
import numpy as np
import pandas as pd
import os
import shutil
from collections import defaultdict
import matplotlib.pyplot as plt

# Class loads specialized data
class DataWARP:
    """
    A class that loads data from the Wroclaw Algorithms for Real-Time Positioning (GNSS-WARP, Hadaś 2015; Hadas et al. 2019) software.
    The software itself is not available here, but there are ready-made .log files obtained by the indicated
    software in the "DataCatalogs" directory.

    The class loads data in two ways:
    - loads the complete .log file,
    - selects the data by offering to pull only the indicated columns along with swapping the column naming.

    start_range - first day in the Day of Year (DoY) system for analysis
    end_range - last day in the Day of Year (DoY) system for analysis
    include_char - measurement mode (s - static, k - kinematic)

    Bibliography:
    Hadaś T (2015) GNSS-Warp Software for Real-Time Precise Point Positioning. Artif Satell 50(2):59–76.
    https://doi.org/10.1515/arsa-2015-0005

    Hadas T, Kazmierski K, Sośnica K (2019) Performance of Galileo-only dual-frequency absolute positioning using
    the fully serviceable Galileo constellation. GPS Solut 23(4):108. https://doi.org/10.1007/s10291-019-0900-9
    """
    def __init__(self, source_folders, output_folder, station_ids):
        self.source_folders = source_folders
        self.output_folder = output_folder
        self.station_ids = station_ids
        self.data_dict = defaultdict(pd.DataFrame)

    def process_data(self, start_range=None, end_range=None, include_char=None):
        try:
            # Delete the existing destination folder, if it exists
            if os.path.exists(self.output_folder):
                shutil.rmtree(self.output_folder)
            os.makedirs(self.output_folder)  # Create a destination folder

            for source_folder in self.source_folders:
                source_suffix = os.path.basename(source_folder)
                for root, dirs, files in os.walk(source_folder):
                    station_data = defaultdict(pd.DataFrame)
                    for file in files:
                        try:
                            if file.endswith("Est.log"):
                                file_name = os.path.basename(file)
                                station_id = file_name[:4]
                                if station_id in self.station_ids:
                                    file_path = os.path.join(root, file)

                                    # Checking the range of numbers in the file name from character 16 to 19
                                    if start_range is not None and end_range is not None:
                                        file_range = int(file[16:19])
                                        if not (start_range <= file_range <= end_range):
                                            continue

                                    # Check type s or k - 43 character in name
                                    if include_char is not None and file[43] != include_char:
                                        continue

                                    if station_id in station_data:
                                        # If data with the same station ID already exists, include the data
                                        data = pd.read_csv(file_path, sep=';')
                                        data.columns = data.columns.str.replace(" ", "")
                                        station_data[station_id] = pd.concat([station_data[station_id], data],
                                                                             ignore_index=True)
                                    else:
                                        # If data with the same station ID does not exist, create new data
                                        data = pd.read_csv(file_path, sep=';')
                                        data.columns = data.columns.str.replace(" ", "")
                                        station_data[station_id] = data
                        except Exception as file_error:
                            print(f"Error processing file {file}: {file_error}")

                    for station_id, data in station_data.items():
                        data = data.dropna()
                        output_file = os.path.join(self.output_folder, f"{station_id}_{source_suffix}.csv")
                        data.to_csv(output_file, index=False, sep=';')
                        self.data_dict[f"{station_id}_{source_suffix}"] = data

        except Exception as process_data_error:
            print(f"Error processing data: {process_data_error}")

    def get_data(self):
        return self.data_dict

    def selected_data(self):
        # Selected data with load of file
        data_dict_2 = {}
        for k, data in self.data_dict.items():
            try:
                data = data.rename(columns={'RecClkG': 'ClcG', 'RecClkR': 'ClcR', 'RecClkE': 'ClcE', 'RecClkC': 'ClcC',
                                            'TDop': 'mClcG', 'HDop': 'mClcR', 'VDop': 'mClcE', 'GDop': 'mClcC',
                                            'RecN': 'N', 'RecE': 'E', 'RecU': 'U',
                                            'RecmN': 'mN', 'RecmE': 'mE', 'RecmU': 'mU'})
                data['ss'] = np.abs(data['ss'])
                data['date'] = pd.to_datetime(data[['YY', 'MM', 'DD', 'hh', 'mm', 'ss']].astype(str).apply(' '.join, 1),
                                              format='%Y %m %d %H %M %S.0')
                data = data[['date', 'ClcG', 'ClcC', 'mClcE', 'nC', 'U', 'mU']]
                data = data.set_index('date').astype(float)
                data = data.replace([np.inf, -np.inf], np.nan).dropna()
                data_dict_2[k] = data
            except Exception as selected_data_error:
                print(f"Error processing selected data for {k}: {selected_data_error}")
        return self.data_dict, data_dict_2