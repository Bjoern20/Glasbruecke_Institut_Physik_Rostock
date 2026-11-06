"""
Plottfunktionen zum Plotten der Spaltmessungen
Version: Vortlaufende Daten
Autor: Björn Lindqvist
Lizenz: CC-BY
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_time_gap(folder, time, D1, D2, D3, D4, delta_D, xlabel, year_start, year_end, time_style):
    FS = 10
    plt.figure(figsize=(10,6)) #(10,6)
    plt.grid(True)
    plt.plot(time, D1, linestyle='--', linewidth=1.5, color='darkblue')
    plt.plot(time, D2, linestyle='--', linewidth=1.5, color='darkred')
    plt.plot(time, D3, linestyle='--', linewidth=1.5, color='slateblue')
    plt.plot(time, D4, linestyle='--', linewidth=1.5, color='chocolate')
    plt.errorbar(time, D1, yerr=delta_D, marker='x', linestyle='None', color='darkblue', markersize=4, markeredgewidth=1, capsize=2.5, label='Measuring point left')
    plt.errorbar(time, D2, yerr=delta_D, marker='+', linestyle='None', color='darkred', markersize=4, markeredgewidth=1, capsize=2.5, label='Measuring point right')
    plt.errorbar(time, D3, yerr=delta_D, marker='x', linestyle='None', color='slateblue', markersize=4, markeredgewidth=1, capsize=2.5, label='Measuring point left new')
    plt.errorbar(time, D4, yerr=delta_D, marker='+', linestyle='None', color='chocolate', markersize=4, markeredgewidth=1, capsize=2.5, label='Measuring point right new')
    if time_style == 'days':
        for i in range(1, int(1000 // 365.25) + 1):
            plt.axvline(x=365.25*i,linestyle='-.', color='darkgray')
    elif time_style == 'time':
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.xticks(rotation=45, ha='right')
    else: 
        print('Wrong time_key!')
    plt.tick_params(axis='x', which='both', labelsize=FS)
    plt.tick_params(axis='y', which='both', labelsize=FS)
    plt.ylim([18,35])
    plt.xlabel(xlabel, fontsize=FS)
    plt.ylabel('Gap distance [mm]', fontsize=FS)
    plt.title('Translatoric movment of the glass bridge at Institute for physics, University of Rostock', fontsize=1.3*FS)
    plt.text(0.11, 0.02, f'Björn Lindqvist ({year_start} - {year_end})', fontsize=0.8*FS, ha='center', va='bottom', transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, boxstyle='round,pad=0.3'))
    plt.legend(fontsize=FS)
    plt.savefig(f'{folder}/Movment.png', dpi=150)
    plt.show()
    return None

#%% sheerment over the year
def plot_sheer(folder, time, D1, D2, D3, D4, delta_D, xlabel, year_start, year_end, time_style):
    sheer12 = D1-D2
    sheer34 = D3-D4
    delta_sheer = delta_D + delta_D
    
    FS = 10
    plt.figure(figsize=(10,6)) #(10,6)
    plt.grid(True)
    plt.errorbar(time, sheer12, yerr=delta_sheer, marker='+', linestyle='--', linewidth=1.5, color='darkgreen', markersize=9, markeredgewidth=2.5, capsize=5, label='old data')
    plt.errorbar(time, sheer34, yerr=delta_sheer, marker='+', linestyle='--', linewidth=1.5, color='limegreen', markersize=9, markeredgewidth=2.5, capsize=5, label='new data')
    if time_style == 'days':
        for i in range(1, int(1000 // 365.25) + 1):
            plt.axvline(x=365.25*i, linestyle='-.', color='darkgray')
    elif time_style == 'time':
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.xticks(rotation=45, ha='right')
    else: 
        print('Wrong time_key!')
    plt.tick_params(axis='x', which='both', labelsize=FS)
    plt.tick_params(axis='y', which='both', labelsize=FS)
    plt.xlabel(xlabel, fontsize=FS)
    plt.ylabel('Sheere distance [mm]', fontsize=FS)
    plt.ylim([0, 1.5*np.nanmax(D1-D2)])
    plt.title('Sheer movment of the glass bridge at Institute for physics, University of Rostock', fontsize=1.3*FS)
    plt.text(0.11, 0.02, f'Björn Lindqvist ({year_start} - {year_end})', fontsize=0.8*FS, ha='center', va='bottom', transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, boxstyle='round,pad=0.3'))
    plt.legend(fontsize=FS)
    plt.savefig(f'{folder}/Sheerment.png', dpi=150)
    plt.show()
    return None


#%% temperature plot
def plot_temperature_movement(folder, T1, T2, D1, D2, D3, D4, delta_T, delta_D, year_start, year_end):
    ext_D = 0.05 #axis scaling in x-dir
    ext_T = 0.10 #axis scaling in y-dir

    FS = 10
    fig, ax = plt.subplots(figsize=(10, 6)) #(10,6)
    gradient = np.linspace(1, 0, 256).reshape(1, -1)
    ax.imshow(gradient, extent=[(1-ext_T)*min(min(T1-delta_T), min(T2-delta_T)), (1+ext_T)*max(max(T1+delta_T), max(T2+delta_T)), (1-ext_D)*min(min(D1-delta_D), min(D2-delta_D)), (1+ext_D)*max(max(D1+delta_D), max(D2+delta_D))], aspect='auto', cmap='coolwarm_r', alpha=0.7)
    plt.errorbar(T1, D1, xerr=delta_T, yerr=delta_D, marker='o', linestyle='', linewidth=1.5, color='darkblue', markersize=5, markeredgewidth=1.5, capsize=5, label='Measuring point left')
    plt.errorbar(T2, D2, xerr=delta_T, yerr=delta_D, marker='v', linestyle='', linewidth=1.5, color='darkred', markersize=5, markeredgewidth=1.5, capsize=5, label='Measuring point right')
    plt.errorbar(T1, D3, xerr=delta_T, yerr=delta_D, marker='o', linestyle='', linewidth=1.5, color='slateblue', markersize=5, markeredgewidth=1.5, capsize=5, label='Measuring point left new')
    plt.errorbar(T2, D4, xerr=delta_T, yerr=delta_D, marker='v', linestyle='', linewidth=1.5, color='chocolate', markersize=5, markeredgewidth=1.5, capsize=5, label='Measuring point right new')
    plt.tick_params(axis='x', which='both', labelsize=FS)
    plt.tick_params(axis='y', which='both', labelsize=FS)
    plt.xlabel('Temperature [°C]', fontsize=FS)
    plt.ylabel('Gap distance [mm]', fontsize=FS)
    plt.title('Temperature dependency for the translatoric movement of the glass bridge \n Institute for Physics, University of Rostock', fontsize=1.3*FS)
    plt.text(0.11, 0.02, f'Björn Lindqvist ({year_start} - {year_end})', fontsize=0.8*FS, ha='center', va='bottom', transform=plt.gca().transAxes)
    plt.legend(fontsize=FS)
    plt.savefig(f'{folder}/Temperature_movment.png', dpi=150)
    plt.show()
    return None