# Libraries
from src.Modules._2_ReadFileLog.readFileLog import DataWARP as dWARP
import os
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import timedelta

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
#print(data_raw)
print(data_selected)
print(type(data_selected))

# Path to save .png files
patch_save_to_png_file_period_1 = os.path.join(os.path.abspath(os.path.join(os.getcwd(), '..', '..')), 'src',
                                               'DataCatalogs', 'ChartFiles')
# Create a charts for the selected data
for station_id, df in data_selected.items():
    # Calculate statistics
    U_mean = df['U'].mean()
    U_std = df['U'].std()
    U_min = df['U'].min()
    U_max = df['U'].max()

    mU_mean = df['mU'].mean()
    mU_std = df['mU'].std()
    mU_min = df['mU'].min()
    mU_max = df['mU'].max()

    # Plotting for column 'U'
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['U'], label='U', color='blue')
    plt.title(f'{station_id} - U')
    plt.xlabel('[month-day hour]')
    plt.ylabel('U [m]')
    plt.legend()
    plt.grid(True)
    plt.text(df.index[0], df['U'].max(), f'Mean: {U_mean:.2f}m\nStd: {U_std:.2f}m\nMin: {U_min:.2f}m\nMax: {U_max:.2f}m',
             fontsize=10, verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.5))
    plt.savefig(os.path.join(patch_save_to_png_file_period_1, f'{station_id}_U.png'))
    plt.show()

    # Plotting for column 'mU'
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['mU'], label='mU', color='red')
    plt.title(f'{station_id} - mU')
    plt.xlabel('[month-day hour]')
    plt.ylabel('mU [m]]')
    plt.legend()
    plt.grid(True)
    plt.text(df.index[0], df['mU'].max(), f'Mean: {mU_mean:.2f}m\nStd: {mU_std:.2f}m\nMin: {mU_min:.2f}m\nMax: {mU_max:.2f}m',
             fontsize=10, verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.5))
    plt.savefig(os.path.join(patch_save_to_png_file_period_1, f'{station_id}_mU.png'))
    plt.show()

convergenceTime = data_selected
for station_id, df in convergenceTime.items():
    X = df.index.astype('int64').values.reshape(-1, 1)
    y = df['mU'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f'Model score for {station_id}: {score}')

    threshold = 0.20
    time_delta = timedelta(seconds=model.intercept_ / threshold)
    print(f'Time to reach mU < {threshold} for {station_id}: {time_delta}')

    y_pred = model.predict(X_test)

    plt.figure(figsize=(10, 6))
    plt.scatter(X_test, y_test, color='blue', label='Actual Data')
    plt.plot(X_test, y_pred, color='red', linewidth=2, label='Linear Regression')
    plt.title(f'Linear Regression for {station_id}')
    plt.xlabel('Date')
    plt.ylabel('mU [m]')
    plt.legend()
    plt.grid(True)
    plt.show()