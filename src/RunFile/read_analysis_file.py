# Libraries
from src.Modules._2_ReadFileLog.readFileLog import DataWARP as dWARP
import os

# Path to load .log files
patch_load_to_log_file_period_1 = os.path.join(os.path.abspath(os.path.join(os.getcwd(), '..', '..')), 'src',
                                               'DataCatalogs', 'LogFiles', 'Period_1')
print(patch_load_to_log_file_period_1)
patch_load_to_log_file_period_2 = os.path.join(os.path.abspath(os.path.join(os.getcwd(), '..', '..')), 'src',
                                               'DataCatalogs', 'LogFiles', 'Period_2')
print(patch_load_to_log_file_period_2)
source_folders = [patch_load_to_log_file_period_1, patch_load_to_log_file_period_2]

# Path to save RNX files
patch_save_to_log_files = os.path.join(os.path.abspath(os.path.join(os.getcwd(), '..', '..')), 'src', 'DataCatalogs', 'RunFiles')
print(patch_save_to_log_files)

# Selected stations
station_ids = ['PTBB', 'BOR1']

# Loading data
data_warp = dWARP(source_folders, patch_save_to_log_files, station_ids)
data_warp.process_data(start_range=244, end_range=246, include_char='s')
data_raw = data_warp.get_data() # load a raw data with file
data_selected = data_warp.selected_data() # load a selected data with file
print(data_raw)
print(data_selected)