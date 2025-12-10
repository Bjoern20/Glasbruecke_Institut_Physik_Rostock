"""
Plottfunktionen zum Plotten der Spaltmessungen
Version: Weihnachtskolloguium 2025
Autor: Björn Lindqvist
Lizenz: CC-BY
"""

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import matplotlib.dates as mdates
import numpy as np

#for presentation set dpi=1000 to get nice marker resolutions

def plot_time_gap(folder, time, D1, D2, delta_D, xlabel, year_start=None, year_end=None, time_style='days', marker_img1=None, marker_img2=None, zoom=0.015):
    FS = 10
    c1 = 'firebrick'
    c2 = 'goldenrod'
    
    plt.figure(figsize=(7,6))
    plt.grid(True)
    plt.plot(time, D1, linestyle='--', linewidth=1, color=c1)
    plt.plot(time, D2, linestyle='--', linewidth=1, color=c2)

    ax = plt.gca()

    # linke Marker
    if marker_img1 is not None:
        img_left = mpimg.imread(marker_img1)
        for xi, yi in zip(time, D1):
            im = OffsetImage(img_left, zoom=zoom)
            ab = AnnotationBbox(im, (xi, yi), frameon=False)
            ax.add_artist(ab)
    
    ax.errorbar(time, D1, yerr=delta_D, marker=None, linestyle='None', color=c1, capsize=2, label='linker Messpunkt')

    # rechte Marker
    if marker_img2 is not None:
        img_right = mpimg.imread(marker_img2)
        for xi, yi in zip(time, D2):
            im = OffsetImage(img_right, zoom=zoom)
            ab = AnnotationBbox(im, (xi, yi), frameon=False)
            ax.add_artist(ab)
    
    ax.errorbar(time, D2, yerr=delta_D, marker=None, linestyle='None', color=c2, capsize=2.5, label='rechter Messpunkt')

    if time_style == 'days':
        plt.axvline(x=365, label='1. year')
    else:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.xticks(rotation=45, ha='right')

    plt.tick_params(axis='x', which='both', labelsize=FS)
    plt.tick_params(axis='y', which='both', labelsize=FS)
    plt.ylim([18,33])
    
    if year_start is not None and year_end is not None:
        plt.text(0.19, 0.02, f'Björn Lindqvist ({year_start} - {year_end})', fontsize=0.8*FS, ha='center', va='bottom', transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, boxstyle='round,pad=0.3'))
    
    plt.xlabel(xlabel, fontsize=FS)
    plt.ylabel('Spaltabstand [mm]', fontsize=FS)
    plt.legend(fontsize=FS)
    plt.savefig(f'{folder}/Movment.png', dpi=150)
    plt.show()
    return None


def plot_sheer(folder, time, D1, D2, delta_D, xlabel, year_start=None, year_end=None, time_style='days', marker_img=None, zoom=0.015):
    sheer = D1 - D2
    delta_sheer = delta_D + delta_D
    FS = 10
    plt.figure(figsize=(7,6))
    plt.grid(True)
    ax = plt.gca()

    if marker_img is not None:
        img = mpimg.imread(marker_img)
        for xi, yi, ye in zip(time, sheer, delta_sheer):
            # optional: Errorbars als Linien
            ax.vlines(x=xi, ymin=yi-ye, ymax=yi+ye, color='green', linewidth=1.5)
            im = OffsetImage(img, zoom=zoom)
            ab = AnnotationBbox(im, (xi, yi), frameon=False)
            ax.add_artist(ab)
        ax.plot(time, sheer, linestyle='--', linewidth=1, color='green')  # Linie zwischen Markern

    ax.errorbar(time, sheer, yerr=delta_sheer, marker=None, linestyle='--',linewidth=1, color='green', capsize=4)

    if time_style == 'days':
        plt.axvline(x=365, label='1. year')
    else:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.xticks(rotation=45, ha='right')

    plt.tick_params(axis='x', which='both', labelsize=FS)
    plt.tick_params(axis='y', which='both', labelsize=FS)
    plt.xlabel(xlabel, fontsize=FS)
    plt.ylabel('Scherung [mm]', fontsize=FS)
    plt.ylim([0, 1.5 * np.nanmax(D1 - D2)])

    if year_start is not None and year_end is not None:
        plt.text(0.19, 0.02, f'Björn Lindqvist ({year_start} - {year_end})', fontsize=0.8*FS, ha='center', va='bottom', transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, boxstyle='round,pad=0.3'))
    
    plt.savefig(f'{folder}/Sheerment.png', dpi=150)
    plt.show()
    return None


def plot_temperature_movement(folder, D1, T1, D2, T2, delta_D, delta_T, year_start=None, year_end=None, marker_img1=None, marker_img2=None, z1=0.01, z2=0.01):
    ext_D = 0.05
    ext_T = 0.10
    FS = 10
    c1 = 'firebrick'
    c2 = 'goldenrod'
    
    fig, ax = plt.subplots(figsize=(11, 6))
    plt.grid(True)

    D_min = min(np.min(D1 - delta_D), np.min(D2 - delta_D))
    D_max = max(np.max(D1 + delta_D), np.max(D2 + delta_D))
    T_min = min(np.min(T1 - delta_T), np.min(T2 - delta_T))
    T_max = max(np.max(T1 + delta_T), np.max(T2 + delta_T))

    D_range = [ (1-ext_D)*D_min, (1+ext_D)*D_max ]
    T_range = [ (1-ext_T)*T_min, (1+ext_T)*T_max ]

    gradient = np.linspace(0, 1, 256).reshape(-1, 1)
    ax.imshow(gradient, extent=[D_range[0], D_range[1], T_range[0], T_range[1]], aspect='auto', cmap='coolwarm_r', alpha=0.7)

    # linke Marker
    if marker_img1 is not None:
        img_left = mpimg.imread(marker_img1)
        for xi, yi in zip(D1, T1):
            im = OffsetImage(img_left, zoom=z1)
            ab = AnnotationBbox(im, (xi, yi), frameon=False)
            ax.add_artist(ab)
            
    plt.errorbar(D1, T1, yerr=delta_T, xerr=delta_D, marker=None, linestyle='', linewidth=1, color=c1, capsize=2, label='linker Messpunkt')

    # rechte Marker
    if marker_img2 is not None:
        img_right = mpimg.imread(marker_img2)
        for xi, yi in zip(D2, T2):
            im = OffsetImage(img_right, zoom=z2)
            ab = AnnotationBbox(im, (xi, yi), frameon=False)
            ax.add_artist(ab)
            
    plt.errorbar(D2, T2, yerr=delta_T, xerr=delta_D, marker=None, linestyle='', linewidth=1, color=c2, capsize=2, label='rechter Messpunkt')

    plt.tick_params(axis='x', which='both', labelsize=FS)
    plt.tick_params(axis='y', which='both', labelsize=FS)
    plt.xlabel('Spaltabstand [mm]', fontsize=FS)
    plt.ylabel('Temperatur [°C]', fontsize=FS)

    if year_start is not None and year_end is not None:
        plt.text(0.11, 0.02, f'Björn Lindqvist ({year_start} - {year_end})',
                 fontsize=0.8*FS, ha='center', va='bottom', transform=ax.transAxes)

    plt.legend(fontsize=FS)
    plt.savefig(f'{folder}/Temperature_movment.png', dpi=150)
    plt.show()
    return None


