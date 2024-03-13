# Libraries
from src.Modules._3_HTML_JSON_data.HTML_JSON import HTMLDownloader as html_1
import os

# Path to save RNX files
patch_save_to_log_files = os.path.join(os.path.abspath(os.path.join(os.getcwd(), '..', '..')), 'src', 'DataCatalogs', 'HTML_JSON_Files')
print(patch_save_to_log_files)

# Link to the website
my_url = "https://network.igs.org/"

# Downloading information from the indicated site
html_downloader = html_1(my_url, patch_save_to_log_files)
unique_th_values = html_downloader.get_unique_th_values()
print(unique_th_values)