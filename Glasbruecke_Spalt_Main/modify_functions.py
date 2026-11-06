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


def data_modifier(file_path_raw):
    df = pd.read_excel(file_path_raw)
    # creat copy of raw data excel 
    
    
    T1_new, T2_new = temperatur_correction(file_path_raw, plot_tick=False)
        

    

    return file_path_raw







