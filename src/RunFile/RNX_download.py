# Libraries
from src.Modules._1_DownloadRNX.downloadRNX import DownloadRNX as dRNX
from src.Modules._1_DownloadRNX.downloadRNX import ModifiedDay as mday
import os

# Path to save RNX files
patch_save_to_rnxfiles = os.path.join(os.path.abspath(os.path.join(os.getcwd(), '..', '..')), 'src', 'DataCatalogs', 'RNXFiles')
print(patch_save_to_rnxfiles)

# Day of Year (DOY) and stations
modified_day_instance = mday(244, 246)
modified_day_list = modified_day_instance.generate_list()
list_of_station = ['PTBB','BOR1']

# The code that runs the sentence
data_analysis = dRNX(
    patch_save_to_rnxfiles,
    'gdc.cddis.eosdis.nasa.gov',
    'anonymous',
    'email',
    f'/gnss/data/daily/',
    [2023],
    modified_day_list,
    list_of_station
)
data_analysis.download_rinex_files()