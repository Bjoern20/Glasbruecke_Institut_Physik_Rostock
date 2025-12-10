"""
Main file zum Plotten der Spaltmessungen
Version: Weihnachtskolloguium 2025
Autor: Björn Lindqvist
Lizenz: CC-BY
"""

import pandas as pd
import os
import locale
locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
import plot_functions_Weihnachts_Koll as fun

file_path = 'Glasbruecke_data_Weihnachtskoll.xlsx'
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
time_style = 'time' #time (days/time)

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
fun.plot_time_gap(folder, time, D1, D2, delta_D, xlabel, year_start=year_start, year_end=year_end, time_style=time_style, marker_img1='Marker/ball.png', marker_img2='Marker/star.png', zoom=0.006)
# fun.plot_time_gap(time, D1, D2, delta_D, xlabel, year_start=year_start, year_end=year_end, time_style=time_style, marker_img1=None, marker_img2=None, zoom=0.006)


#%% sheerment over the year
print('INFO: plot time-sheer')
fun.plot_sheer(folder, time, D1, D2, delta_D, xlabel, year_start=year_start, year_end=year_end, time_style=time_style, marker_img='Marker/tree.png', zoom=0.015)
# fun.plot_sheer(time, D1, D2, delta_D, xlabel, year_start=year_start, year_end=year_end, time_style=time_style, marker_img=None, zoom=0.015)

#%% temperature plot
print('INFO: plot temp-gap')
fun.plot_temperature_movement(folder, D1, T1, D2, T2, delta_D, delta_T, year_start=year_start, year_end=year_end, marker_img1='Marker/ball.png', marker_img2='Marker/star.png', z1=0.008, z2=0.010)
# fun.plot_temperature_movement(D1, T1, D2, T2, delta_D, delta_T, year_start=None, year_end=None, marker_img1=None, marker_img2=None, zoom=0.006)


print('Exitcode 0')








