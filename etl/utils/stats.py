from __future__ import annotations
import numpy as np

def zscore(values, cap=3.0):
    v = np.asarray(values, dtype=float)
    m = np.nanmean(v)
    s = np.nanstd(v)
    if s == 0 or np.isnan(s):
        z = np.zeros_like(v)
    else:
        z = (v - m) / s
    if cap is not None:
        z = np.clip(z, -cap, cap)
    return z

def scale01(arr):
    a = np.asarray(arr, dtype=float)
    amin, amax = np.nanmin(a), np.nanmax(a)
    if not np.isfinite(amin) or not np.isfinite(amax) or amin == amax:
        return np.zeros_like(a)
    return (a - amin) / (amax - amin)
