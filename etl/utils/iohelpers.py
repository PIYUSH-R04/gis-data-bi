from __future__ import annotations
import os, sys, math
from pathlib import Path
import requests
from tqdm import tqdm

def ensure_dir(p: str | Path) -> Path:
    pa = Path(p)
    pa.mkdir(parents=True, exist_ok=True)
    return pa

def month_parts(ym: str) -> tuple[int,int,str,str]:
    y = int(ym.split("-")[0]); m = int(ym.split("-")[1])
    return y, m, f"{m:02d}", f"{y:04d}"

def stream_download(url: str, out_path: Path, chunk: int = 1024 * 1024) -> Path:
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with tqdm(total=total, unit="B", unit_scale=True, desc=out_path.name) as pbar:
            with open(out_path, "wb") as f:
                for chunk_bytes in r.iter_content(chunk_size=chunk):
                    if chunk_bytes:
                        f.write(chunk_bytes)
                        pbar.update(len(chunk_bytes))
    return out_path
