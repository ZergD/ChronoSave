"""
I gave the main.py to ChatGPT 5 and this is his improvement.
"""


from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple, Dict
import datetime as dt
import hashlib
import shutil

from pprint import pprint

import logging
from logging_setup import setup_logging
from log_utils import section, kv, table, row
from rich.table import Table
from rich.console import Console
from rich.box import MINIMAL_DOUBLE_HEAD

console = Console()


logger = setup_logging(level="INFO", log_file="run.log", json_file=None)


@dataclass(frozen=True)
class Filename:
    fullpath: Path
    hashfile: str
    last_updated: dt.datetime

    def __repr__(self) -> str:
        return (
            f"- file: {self.fullpath}\n"
            f"- with hash: {self.hashfile},\n"
            f"- last updated on: {self.last_updated.isoformat(timespec='seconds')}"
        )


# ---------- public API ----------

# def fetch_needed_files(base: Path | None = None, pattern: str = "*.txt") -> Tuple[List[Filename], List[Filename]]:
#     """
#     Scan base (default: cwd) for files matching `pattern`, and `base/'saves'` for saved copies.
#     Returns: (current_result_bag, saved_result_bag)
#     """
#     base = base or Path.cwd()
#     saves_path = base / "saves"
#     saves_path.mkdir(exist_ok=True)
# 
#     current_files = get_files_from_given_path(base, pattern)
#     saved_files = get_files_from_given_path(saves_path, pattern)
# 
#     current_bag = [build_filename(p) for p in current_files]
#     saved_bag = [build_filename(p) for p in saved_files]
# 
#     return current_bag, saved_bag


def fetch_needed_files(base: Path | None = None, pattern: str = "*.txt"):
    base = base or Path.cwd()
    saves = base / "saves"
    saves.mkdir(exist_ok=True)

    section("Scanning for files")
    kv("base", base.resolve())
    kv("pattern", pattern)
    kv("saves dir", saves.resolve())
    print("\n")

    current = get_files_from_given_path(base, pattern)
    saved = get_files_from_given_path(saves, pattern)

    # Build bags (your existing build_filename)
    current_bag = [build_filename(p) for p in current]
    saved_bag = [build_filename(p) for p in saved]

    table("Current files", (row(f) for f in current_bag))
    table("Saved files", (row(f) for f in saved_bag))

    return current_bag, saved_bag


def compute_diff(current_bag: Iterable[Filename], saved_bag: Iterable[Filename], saves_dir: Path, dry_run: bool = False) -> List[Path]:
    """
    For each current file, if no identical saved copy exists (by sha256), copy into saves_dir
    with an incrementing suffix: {stem}__saved_001{suffix}.
    Returns list of created file paths.
    """
    section("Computing diff", "🧮")
    kv("dry_run", dry_run)
    kv("saves_dir", saves_dir.resolve())
    saves_dir.mkdir(parents=True, exist_ok=True)

    # Map: hash -> list of saved paths (quick inclusion test)
    saved_by_hash: Dict[str, List[Path]] = {}
    for s in saved_bag:
        saved_by_hash.setdefault(s.hashfile, []).append(s.fullpath)
    # print("saved_by_hash looks like this:")
    # pprint(saved_by_hash)

    # Next index per base stem
    next_index: Dict[Tuple[str, str], int] = {}
    for s in saved_bag:
        stem, suffix = s.fullpath.stem, s.fullpath.suffix
        base_stem, _idx = split_saved_stem(stem)
        key = (base_stem, suffix)
        idx = _idx or 0
        next_index[key] = max(next_index.get(key, 0), idx)
    #  print("next_index looks like this:")
    #  pprint(next_index)


    created: List[Path] = []

    for cur in current_bag:
        # skip files that already exist in saves by hash
        if cur.hashfile in saved_by_hash:
            continue

        stem, suffix = cur.fullpath.stem, cur.fullpath.suffix
        key = (stem, suffix)
        idx = next_index.get(key, 0) + 1
        next_index[key] = idx

        target = saves_dir / f"{stem}__saved_{idx:03d}{suffix}"

        if not dry_run:
            shutil.copy2(cur.fullpath, target)  # preserves mtime/metadata
        created.append(target)

    if created:
        section("New saves created", "✅")
        table("Created", ({"target": str(p)} for p in created))
        print("\n")
    else:
        logger.info("✅ Nothing to save — everything up to date.\n")

    return created


# ---------- helpers ----------

def build_filename(p: Path) -> Filename:
    return Filename(
        fullpath=p,
        hashfile=get_hashfile(p),
        last_updated=get_latest_modified_timestamp(p),
    )



def print_bag_of_filenames(bag: Iterable[Filename], title: str = "Files") -> None:
    bag = list(bag)
    if not bag:
        console.print(f"[yellow]No files found for {title}[/yellow]")
        return

    table = Table(title=f"{title} ({len(bag)} files)", box=MINIMAL_DOUBLE_HEAD)
    table.add_column("Name", style="cyan", overflow="fold")
    table.add_column("Hash", style="magenta", no_wrap=True)
    table.add_column("Last Updated", style="green")

    for f in bag:
        table.add_row(
            Path(f.fullpath).name,
            f.hashfile[:12] + "…",
            f.last_updated.isoformat(timespec="seconds")
        )

    console.print(table)


def get_hashfile(file: Path) -> str:
    h = hashlib.sha256()
    with file.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def get_latest_modified_timestamp(file: Path) -> dt.datetime:
    return dt.datetime.fromtimestamp(file.stat().st_mtime).astimezone()


def get_files_from_given_path(path: Path, pattern: str = "*.txt") -> List[Path]:
    if not path.exists():
        return []
    # Only files (no dirs), non-recursive. Adjust to rglob if needed.
    return [p for p in path.glob(pattern) if p.is_file()]


def split_saved_stem(stem: str) -> Tuple[str, int | None]:
    """
    Parse 'name__saved_012' -> ('name', 12). Otherwise ('name', None).
    """
    marker = "__saved_"
    if marker in stem:
        base, suffix = stem.rsplit(marker, 1)
        try:
            return base, int(suffix)
        except ValueError:
            return stem, None
    return stem, None


# ---------- script usage ----------

if __name__ == "__main__":
    base = Path.cwd()
    current_bag, saved_bag = fetch_needed_files(base)
    # print("Current result bag:")
    # print_bag_of_filenames(current_bag)
    # print("Saved result bag:")
    # print_bag_of_filenames(saved_bag)

    created = compute_diff(current_bag, saved_bag, base / "saves", dry_run=False)
