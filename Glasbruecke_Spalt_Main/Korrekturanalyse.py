"""
Korrekturterm
Version: Vortlaufende Daten
Autor: Björn Lindqvist
Lizenz: CC-BY
"""

import pandas as pd
import numpy as np
import correction_functions as corr_fun


file_path = 'Glasbruecke_data.xlsx'
df = pd.read_excel(file_path, 'Tabelle2')

T_fit = np.linspace(10, 25, 1000)

fit_T1 = corr_fun.linear_fit(df['T1_old'], df['T1_new'], T_fit)
fit_T2 = corr_fun.linear_fit(df['T2_old'], df['T2_new'], T_fit)

corr_fun.plot_correction(df, fit_T1, fit_T2, T_fit)

print('Exitcode 0')

