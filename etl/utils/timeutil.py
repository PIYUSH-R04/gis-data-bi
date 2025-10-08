from __future__ import annotations
from datetime import datetime, timedelta, timezone

def latest_completed_month() -> str:
    today = datetime.now(timezone.utc).date().replace(day=1)
    last_month = today - timedelta(days=1)
    return f"{last_month.year:04d}-{last_month.month:02d}"

def normalize_month(s: str | None) -> str:
    return latest_completed_month() if not s or s.lower()=="latest" else s
