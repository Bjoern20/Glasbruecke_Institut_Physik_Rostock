import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def linear_fit(x, y, x_fit):
    x = np.asarray(x)
    y = np.asarray(y)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    return {
        "x_fit": x_fit,
        "y_fit": slope * x_fit + intercept,
        "slope": slope,
        "intercept": intercept,
        "r_value": r_value,
        "r_squared": r_value**2,
        "p_value": p_value,
        "std_err": std_err
    }

def plot_correction(df, fit1, fit2, x_ref):
    plt.figure()
    plt.grid(True)
    plt.scatter(df['T1_old'], df['T1_new'], marker='s', label='Data T1')
    plt.plot(
        fit1["x_fit"],
        fit1["y_fit"],
        label=f'Fit T1: f(x)={fit1["slope"]:.2f}x+{fit1["intercept"]:.2f}'
    )
    plt.scatter(df['T2_old'], df['T2_new'], label='Data T2')
    plt.plot(
        fit2["x_fit"],
        fit2["y_fit"],
        label=f'Fit T2: f(x)={fit2["slope"]:.2f}x+{fit2["intercept"]:.2f}'
    )
    plt.plot(x_ref, x_ref, linestyle='--', color='black', linewidth=1, label='ideal behavior: f(x)=x')
    plt.xlim([10, 22])
    plt.xlabel('Old temperature [°C]')
    plt.xlabel('Corrected temperature [°C]')
    plt.title('Correction fit for FLIR/temperature measurement')
    plt.legend()
    plt.show()
    return None