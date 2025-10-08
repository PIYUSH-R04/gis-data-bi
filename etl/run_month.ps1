param(
  [string]$Month = ""  # format: YYYY-MM; empty = latest
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

if (-not (Test-Path .\.venv\Scripts\Activate.ps1)) {
  Write-Host "Python venv missing. Create it first." -ForegroundColor Red
  exit 1
}
.\.venv\Scripts\Activate.ps1

# Phase chain will be populated in the next phases:
# python 10_fetch_monthly.py --month $Month
# python 20_process_monthly.py --month $Month
# python 30_compute_indices.py --month $Month
# python 40_admin_rollups.py --month $Month
# python 50_make_client_slices.py --month $Month

Write-Host "Pipeline skeleton ready. Fill steps in Phase 1–5." -ForegroundColor Green
