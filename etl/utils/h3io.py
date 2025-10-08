from __future__ import annotations
from typing import Tuple
import h3
import numpy as np

def lonlat_to_h3(lon: float, lat: float, res: int) -> str:
    return h3.geo_to_h3(lat, lon, res)

def cell_area_km2(res: int) -> float:
    return h3.cell_area(h3.latlng_to_cell(0,0,res), unit='km^2')  # dummy cell area
