from __future__ import annotations
from typing import Tuple, Optional
import rasterio as rio
import numpy as np

def read_window_mean(path: str, bbox: Tuple[float,float,float,float]) -> Tuple[np.ndarray, dict]:
    """Read a lightweight window; Phase 1 will implement proper windowing."""
    with rio.open(path) as ds:
        arr = ds.read(1, masked=True)
        return np.asarray(arr), ds.meta
