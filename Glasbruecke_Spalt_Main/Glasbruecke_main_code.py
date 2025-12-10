"""
Main file zum Plotten der Spaltmessungen
Version: Vortlaufende Daten
Autor: Björn Lindqvist
Lizenz: CC-BY
"""

import pandas as pd
import os
import plot_functions as fun

file_path = 'Glasbruecke_data.xlsx'
df = pd.read_excel(file_path)

Dates = df['Date']
Days = (df['Date'] - df['Date'][0]).dt.days.to_numpy()
T1 = df['T1/°C'].to_numpy()
T2 = df['T2/°C'].to_numpy()
D1 = df['D1/mm'].to_numpy()
D2 = df['D2/mm'].to_numpy()
delta_T = df['dT_i/K'].to_numpy()
delta_D = df['dD_i/mm'].to_numpy()


year_start = '2024' #only text
year_end = '2025' #only text
time_style = 'time' #time (#days) or Date (date)

if time_style == 'days':
    time = Days
    xlabel = 'Days since first measurement on 15.08.2024'
elif time_style == 'time':
    time = Dates 
    xlabel = 'Date'
else:
    print('Wrong time_key!')
    
folder = 'figures'
os.makedirs(folder, exist_ok=True)


#%% movment over the year
print('INFO: plot time-gap')
fun.plot_time_gap(folder, time, D1, D2, delta_D, xlabel, year_start=year_start, year_end=year_end, time_style=time_style)

#%% sheerment over the year
print('INFO: plot time-sheer')
fun.plot_sheer(folder, time, D1, D2, delta_D, xlabel, year_start=year_start, year_end=year_end, time_style=time_style)

#%% temperature plot
print('INFO: plot temp-gap')
fun.plot_temperature_movement(folder, D1, T1, D2, T2, delta_D, delta_T, year_start=year_start, year_end=year_end)

print('Exitcode 0')








