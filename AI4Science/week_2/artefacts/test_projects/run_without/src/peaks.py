"""Поиск пиков и вычисление FWHM для всех спектров в data/."""
import csv
import glob
import os
import numpy as np
from scipy.signal import find_peaks

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT = os.path.join(os.path.dirname(__file__), "..", "results", "peaks.csv")


def find_fwhm(wavelengths, intensities, peak_idx):
    """Вычислить FWHM пика через интерполяцию половинной высоты."""
    peak_height = intensities[peak_idx]
    half_max = peak_height / 2.0

    # Ищем левую точку на половинной высоте
    left_idx = None
    for i in range(peak_idx, -1, -1):
        if intensities[i] <= half_max:
            # Линейная интерполяция между i и i+1
            if intensities[i + 1] != intensities[i]:
                frac = (half_max - intensities[i]) / (intensities[i + 1] - intensities[i])
                left_wl = wavelengths[i] + frac * (wavelengths[i + 1] - wavelengths[i])
            else:
                left_wl = wavelengths[i]
            left_idx = i
            break

    # Ищем правую точку на половинной высоте
    right_idx = None
    for i in range(peak_idx, len(wavelengths)):
        if intensities[i] <= half_max:
            # Линейная интерполяция между i-1 и i
            if intensities[i] != intensities[i - 1]:
                frac = (half_max - intensities[i - 1]) / (intensities[i] - intensities[i - 1])
                right_wl = wavelengths[i - 1] + frac * (wavelengths[i] - wavelengths[i - 1])
            else:
                right_wl = wavelengths[i]
            right_idx = i
            break

    if left_idx is not None and right_idx is not None:
        return right_wl - left_wl
    return None


def process_spectrum(filepath):
    """Обработать один спектр: найти пики и вычислить FWHM."""
    data = np.loadtxt(filepath, skiprows=1, delimiter="\t")
    wavelengths = data[:, 0]
    intensities = data[:, 1]

    # Находим пики с помощью prominence
    peaks, properties = find_peaks(intensities, prominence=0.05, distance=50)

    results = []
    for peak_idx in peaks:
        fwhm = find_fwhm(wavelengths, intensities, peak_idx)
        if fwhm is not None and fwhm > 0:
            results.append({
                "center_nm": round(wavelengths[peak_idx], 1),
                "fwhm_nm": round(fwhm, 1),
            })

    return results


def main():
    all_results = []
    spectrum_files = sorted(glob.glob(os.path.join(DATA_DIR, "spectrum_*.txt")))

    for filepath in spectrum_files:
        filename = os.path.basename(filepath)
        print(f"Обработка {filename}...")
        peaks = process_spectrum(filepath)
        for p in peaks:
            all_results.append({
                "file": filename,
                "center_nm": p["center_nm"],
                "fwhm_nm": p["fwhm_nm"],
            })
            print(f"  Пик: {p['center_nm']} нм, FWHM: {p['fwhm_nm']} нм")

    # Запись результатов
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "center_nm", "fwhm_nm"])
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\nРезультаты записаны в {OUTPUT}")
    print(f"Всего пиков: {len(all_results)}")


if __name__ == "__main__":
    main()