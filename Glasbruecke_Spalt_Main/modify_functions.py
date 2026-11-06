"""
Hilfsfunktion um Daten aufzubereiten
Version: Vortlaufende Daten
Autor: Björn Lindqvist
Lizenz: CC-BY
"""

import pandas as pd 
import correction_functions as corr_fun
import numpy as np

def temperatur_correction(file_path, plot_tick=False):
    def single_temp_corr(df_tab1, df_tab2, df_tab2_red, T_fit, T_value):
        fit_T = corr_fun.linear_fit(df_tab2_red[f'T{T_value}_old'], df_tab2_red[f'T{T_value}_new'], T_fit)
        T = df_tab1[f'T{T_value}/°C'].to_numpy()
        T_new_fitted = df_tab2[f'T{T_value}_new'] #take new data
        T_new_fitted[0:49] = fit_T['slope']*T[0:49] + fit_T['intercept'] #correct wrong data
        return fit_T, T_new_fitted
    
    
    df_tab1 = pd.read_excel(file_path, 'Tabelle1')
    df_tab2 = pd.read_excel(file_path, 'Tabelle2')
    df_tab2_red = corr_fun.delete_nans(df_tab2)

    T_fit = np.linspace(10, 35, 1000)
    fit_T1, T1_new_fitted = single_temp_corr(df_tab1, df_tab2, df_tab2_red, T_fit, T_value='1')
    fit_T2, T2_new_fitted = single_temp_corr(df_tab1, df_tab2, df_tab2_red, T_fit, T_value='2')
    
    if plot_tick: corr_fun.plot_correction(df_tab2_red, fit_T1, fit_T2, T_fit)

    return T1_new_fitted, T2_new_fitted


#this function do nothing currently and just return input path again
def temperature_modifier(file_path_raw):
    df = pd.read_excel(file_path_raw)
    # creat copy of raw data excel 
    # T1_new, T2_new = temperatur_correction(file_path_raw, plot_tick=False) #this function throw errors as well 
    return file_path_raw


#%% Correct new measurementpoints after closing the gap in summer 2026
def linear_fit(x, y):
    mask = np.isfinite(x) & np.isfinite(y)
    a, b = np.polyfit(x[mask], y[mask], 1)
    return a, b

def debug_plot_linear_fits(T1, T2, D1, D2, D3, D4, a1, a2, a3, a4, b1, b2, b3, b4, main_shift, pos_shift):
    import matplotlib.pyplot as plt
    T_vec = np.linspace(9, 37, 1000)
    plt.figure()
    plt.plot(T1, D1, 's')
    plt.plot(T2, D2, 'o')
    plt.plot(T1, D3-main_shift, '*')
    plt.plot(T2, D4-main_shift-pos_shift, 'x')
    plt.plot(T_vec, a1*T_vec+b1)
    plt.plot(T_vec, a2*T_vec+b2)
    plt.plot(T_vec, a3*T_vec+b3-main_shift)
    plt.plot(T_vec, a4*T_vec+b4-main_shift-pos_shift)
    plt.show()
    return None 

def new_measurmentpoint_modifier(T1, T2, D1, D2, D3, D4, debug_plot_tick=False):
    
    T_reference = np.nanmean([T1, T2])
    
    a1, b1 = linear_fit(T1, D1)
    a2, b2 = linear_fit(T2, D2)
    a3, b3 = linear_fit(T1, D3)
    a4, b4 = linear_fit(T2, D4)
    
    D1_ref = a1*T_reference + b1
    D3_ref = a3*T_reference + b3

    main_shift = D3_ref - D1_ref #schiebt neue Daten ins Optimum der Temp-Gab-Verteilung
    pos_shift = np.nanmean(D4 - D3) + np.nanmean(D1 - D2) #korrigiert den zusammenhang der beiden Messpunkte, da es keine Scherung gibt kann man mittelwerte Bilden und diese einfach subtrahieren (sowohl für alte als auch neue Daten)
    D_new1 = np.where(~np.isnan(D1), D1, D3 - main_shift) #mm
    D_new2 = np.where(~np.isnan(D2), D2, D4 - main_shift - pos_shift) #mm
    
    if debug_plot_tick: 
        debug_plot_linear_fits(T1, T2, D1, D2, D3, D4, a1, a2, a3, a4, b1, b2, b3, b4, main_shift, pos_shift)
    
    return D3 - main_shift, D4 - main_shift - pos_shift
    # return D_new1, D_new2






