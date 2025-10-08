from __future__ import annotations
import yaml, numpy as np, pandas as pd
import shapely, pyproj, rasterio, xarray, rioxarray, h3, pyarrow

def main():
    print("Config load…")
    with open("config.yml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    print("Project:", cfg["project"]["name"])
    print("H3 res :", cfg["project"]["h3_resolution"])
    print("Region :", cfg["region"]["name"])

    a = np.array([1,2,3,4,5], dtype=float)
    print("NumPy ok, mean:", a.mean())

    from shapely.geometry import Point
    p = Point(85.3240, 27.7172)
    print("Shapely ok, point:", p.wkt[:32], "…")

    cell = h3.geo_to_h3(p.y, p.x, cfg["project"]["h3_resolution"])
    print("H3 ok, cell:", cell)

    print("xarray:", xarray.__version__, "rasterio:", rasterio.__version__)
    print("All good")

if __name__ == "__main__":
    main()
