from __future__ import annotations
import argparse, json, yaml, sys
from pathlib import Path
from utils.iohelpers import ensure_dir, month_parts, stream_download
from utils.timeutil import normalize_month

def load_cfg() -> dict:
    with open("config.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def chirps_fetch(cfg: dict, ym: str, year_dir: Path) -> Path | None:
    """Download CHIRPS per-year NetCDF containing all 12 months.
    We store it under data/raw/YYYY/chirps-v2.0.YYYY.monthly.nc
    """
    from utils.iohelpers import stream_download
    from utils.iohelpers import month_parts

    yyyy, mm, MM, YYYY = month_parts(ym)
    src = cfg["sources"]["chirps_monthly"]
    url = src["template_by_year"].replace("{YYYY}", YYYY)
    out_path = year_dir / f"chirps-v2.0.{YYYY}.monthly.nc"

    if out_path.exists():
        print(f"[CHIRPS] Exists: {out_path}")
        return out_path

    try:
        print(f"[CHIRPS] Downloading: {url}")
        stream_download(url, out_path)
        print(f"[CHIRPS] Saved: {out_path}")
        return out_path
    except Exception as e:
        print(f"[CHIRPS] WARN (byYear failed): {e}")

        alt = src.get("alt_whole_series")
        if alt:
            try:
                print(f"[CHIRPS] Trying alt whole-series: {alt}")
                stream_download(alt, out_path.with_name("chirps-v2.0.monthly.nc"))
                print(f"[CHIRPS] Saved alt: {out_path.with_name('chirps-v2.0.monthly.nc')}")
                return out_path.with_name("chirps-v2.0.monthly.nc")
            except Exception as e2:
                print(f"[CHIRPS] WARN (alt failed): {e2}")

        return None

def placeholder_notice(dataset_name: str, expected_ext: str, target_dir: Path, filename_hint: str):
    print(f"[{dataset_name}] No auto-download implemented yet.")
    print(f"  Place a file named like '{filename_hint}{expected_ext}' in: {target_dir}")
    print(f"  Skipping for now.\n")

def ndvi_placeholder(cfg: dict, ym: str, out_dir: Path) -> Path | None:
    expected_ext = cfg["sources"]["modis_ndvi_monthly"]["expected_ext"]
    p = out_dir / f"ndvi_{ym}{expected_ext}"
    if p.exists():
        print(f"[NDVI] Found: {p}")
        return p
    placeholder_notice("NDVI", expected_ext, out_dir, f"ndvi_{ym}")
    return None

def fire_placeholder(cfg: dict, ym: str, out_dir: Path) -> Path | None:
    expected_ext = cfg["sources"]["modis_fire_monthly"]["expected_ext"]
    p = out_dir / f"fire_{ym}{expected_ext}"
    if p.exists():
        print(f"[FIRE] Found: {p}")
        return p
    placeholder_notice("FIRE", expected_ext, out_dir, f"fire_{ym}")
    return None

def viirs_placeholder(cfg: dict, ym: str, out_dir: Path) -> Path | None:
    expected_ext = cfg["sources"]["viirs_nl_monthly"]["expected_ext"]
    p = out_dir / f"viirs_nl_{ym}{expected_ext}"
    if p.exists():
        print(f"[VIIRS NL] Found: {p}")
        return p
    placeholder_notice("VIIRS_NL", expected_ext, out_dir, f"viirs_nl_{ym}")
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", type=str, default="latest", help='YYYY-MM or "latest"')
    args = ap.parse_args()
    ym = normalize_month(args.month)

    cfg = load_cfg()
    base_data = Path(cfg["project"]["base_dir"]) / "data" / "raw"

    yyyy = ym.split("-")[0]
    year_dir = ensure_dir(base_data / yyyy)
    month_dir = ensure_dir(base_data / ym.replace("-", "/"))

    manifest = {"month": ym, "artifacts": {}}

    chirps_file = chirps_fetch(cfg, ym, year_dir)
    if chirps_file:
        manifest["artifacts"]["chirps_year_nc"] = str(chirps_file.resolve())

    ndvi_file = ndvi_placeholder(cfg, ym, month_dir)
    if ndvi_file:
        manifest["artifacts"]["ndvi"] = str(ndvi_file.resolve())

    fire_file = fire_placeholder(cfg, ym, month_dir)
    if fire_file:
        manifest["artifacts"]["fire"] = str(fire_file.resolve())

    viirs_file = viirs_placeholder(cfg, ym, month_dir)
    if viirs_file:
        manifest["artifacts"]["viirs_nl"] = str(viirs_file.resolve())

    mpath = month_dir / "_manifest.json"
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"[OK] Manifest: {mpath}")


if __name__ == "__main__":
    main()
