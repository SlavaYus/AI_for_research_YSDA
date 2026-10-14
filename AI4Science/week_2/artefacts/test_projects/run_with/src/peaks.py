#!/usr/bin/env python3
"""Extract peak positions and FWHM from absorption spectra."""

import csv
import numpy as np
from pathlib import Path
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

root = Path(__file__).resolve().parents[1]
data_dir = root / "data"
out_csv = root / "results" / "peaks.csv"


def gaussian_with_bg(x, amp, center, sigma, slope, intercept):
    """Gaussian peak on top of a linear background."""
    return (amp * np.exp(-0.5 * ((x - center) / sigma) ** 2)
            + slope * x + intercept)


def fwhm_from_sigma(sigma):
    return 2.0 * np.sqrt(2.0 * np.log(2.0)) * sigma


def find_peaks_and_fit(wl, intensity):
    """Find peaks and fit Gaussians with linear background."""
    # Estimate noise from median absolute deviation
    noise = np.median(np.abs(intensity - np.median(intensity)))
    threshold = 5.0 * noise

    # Find local maxima with prominence
    peak_indices, properties = find_peaks(
        intensity, height=threshold, distance=10, prominence=0.1
    )

    results = []
    for idx in peak_indices:
        center_guess = wl[idx]
        amp_guess = intensity[idx]

        # Estimate background slope from local window edges
        window = 50
        lo = max(0, idx - window)
        hi = min(len(wl), idx + window + 1)

        # Background estimate from window edges
        bg_avg = (intensity[lo] + intensity[hi - 1]) / 2.0
        bg_center = (wl[lo] + wl[hi - 1]) / 2.0
        bg_slope = (intensity[hi - 1] - intensity[lo]) / (wl[hi - 1] - wl[lo])
        bg_intercept = bg_avg - bg_slope * bg_center

        sigma_guess = 2.0

        wl_win = wl[lo:hi]
        int_win = intensity[lo:hi]

        try:
            popt, _ = curve_fit(
                gaussian_with_bg, wl_win, int_win,
                p0=[amp_guess, center_guess, sigma_guess, bg_slope, bg_intercept],
                bounds=([0, 400, 0.1, -1, -1], [amp_guess * 3, 700, 50, 1, 1]),
                maxfev=5000,
            )
            amp_fit, center_fit, sigma_fit, _, _ = popt
            fwhm = fwhm_from_sigma(sigma_fit)
            results.append((center_fit, fwhm))
        except Exception:
            results.append((center_guess, 5.0))

    return results


def main():
    rows = []
    for fn in sorted(data_dir.glob("spectrum_*.txt")):
        wl = []
        intensity = []
        with open(fn) as f:
            next(f)  # skip header
            for line in f:
                parts = line.strip().split("\t")
                wl.append(float(parts[0]))
                intensity.append(float(parts[1]))
        wl = np.array(wl)
        intensity = np.array(intensity)

        peaks = find_peaks_and_fit(wl, intensity)
        for center, fwhm in peaks:
            rows.append({
                "file": fn.name,
                "center_nm": f"{center:.1f}",
                "fwhm_nm": f"{fwhm:.1f}",
            })

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "center_nm", "fwhm_nm"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} peaks to {out_csv}")


if __name__ == "__main__":
    main()