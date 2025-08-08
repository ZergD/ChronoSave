# log_utils.py
from __future__ import annotations
import logging
from typing import Iterable
from dataclasses import asdict, is_dataclass

log = logging.getLogger("filesync")

def section(title: str, emoji: str = "📂") -> None:
    log.info("")
    log.info(f"{emoji} [bold]%s[/bold]", title)  # Rich markup if available
    log.info("—" * 60)

def kv(key: str, value) -> None:
    log.info("[dim]%s[/dim]: %s", key, value)

def table(title: str, rows: Iterable[dict]) -> None:
    try:
        from rich.table import Table
        from rich.console import Console
        rows = list(rows)
        if not rows:
            section(f"{title} (empty)", "🗒️")
            return
        cols = list(rows[0].keys())
        t = Table(title=title)
        for c in cols: t.add_column(c)
        for r in rows: t.add_row(*(str(r.get(c, "")) for c in cols))
        Console().print(t)
    except Exception:
        # Fallback text
        section(title, "🗒️")
        for r in rows:
            log.info(" • " + " | ".join(f"{k}={v}" for k, v in r.items()))

def row(obj) -> dict:
    if is_dataclass(obj):
        d = asdict(obj)
    elif hasattr(obj, "__dict__"):
        d = obj.__dict__.copy()
    else:
        d = dict(obj)
    # compact/pretty tweaks
    if "hashfile" in d:
        d["hash8"] = str(d.pop("hashfile"))[:8]
    if "last_updated" in d:
        d["last_updated"] = getattr(d["last_updated"], "isoformat", lambda: d["last_updated"])()
    if "fullpath" in d:
        d["name"] = str(d["fullpath"].name)
        d["path"] = str(d.pop("fullpath"))
    return d
