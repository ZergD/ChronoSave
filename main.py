from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple, Dict
import argparse
import sys
import datetime as dt
import hashlib
import shutil
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


def fetch_needed_files(base: Path | None = None, pattern: str = "*.txt"):
    base = base or Path.cwd()
    saves = base / "saves"
    saves.mkdir(exist_ok=True)

    section("Scanning for files")
    kv("base", base.resolve())
    kv("pattern", pattern)
    kv("saves dir", saves.resolve())
    print()

    current = get_files_from_given_path(base, pattern)
    saved = get_files_from_given_path(saves, pattern)

    current_bag = [build_filename(p) for p in current]
    saved_bag = [build_filename(p) for p in saved]

    table("Current files", (row(f) for f in current_bag))
    table("Saved files", (row(f) for f in saved_bag))

    return current_bag, saved_bag


def compute_diff(current_bag: Iterable[Filename], saved_bag: Iterable[Filename], saves_dir: Path, dry_run: bool = False) -> List[Path]:
    section("Computing diff", "🧮")
    kv("dry_run", dry_run)
    kv("saves_dir", saves_dir.resolve())
    saves_dir.mkdir(parents=True, exist_ok=True)

    saved_by_hash: Dict[str, List[Path]] = {}
    for s in saved_bag:
        saved_by_hash.setdefault(s.hashfile, []).append(s.fullpath)

    next_index: Dict[Tuple[str, str], int] = {}
    for s in saved_bag:
        stem, suffix = s.fullpath.stem, s.fullpath.suffix
        base_stem, _idx = split_saved_stem(stem)
        key = (base_stem, suffix)
        idx = _idx or 0
        next_index[key] = max(next_index.get(key, 0), idx)

    created: List[Path] = []

    for cur in current_bag:
        if cur.hashfile in saved_by_hash:
            continue

        stem, suffix = cur.fullpath.stem, cur.fullpath.suffix
        key = (stem, suffix)
        idx = next_index.get(key, 0) + 1
        next_index[key] = idx

        target = saves_dir / f"{stem}__saved_{idx:03d}{suffix}"

        if not dry_run:
            shutil.copy2(cur.fullpath, target)
        created.append(target)

    if created:
        section("New saves created", "✅")
        table("Created", ({"target": str(p)} for p in created))
        print()
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
    files: List[Path] = [p for p in path.glob(pattern) if p.is_file()]
    # exclude requirements.txt explicitly
    return [p for p in files if p.name != "requirements.txt"]


def split_saved_stem(stem: str) -> Tuple[str, int | None]:
    marker = "__saved_"
    if marker in stem:
        base, suffix = stem.rsplit(marker, 1)
        try:
            return base, int(suffix)
        except ValueError:
            return stem, None
    return stem, None


# ---------- CLI ----------

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="chronosave",
        description="ChronoSave — detect file changes and save versioned copies."
    )
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Folder to scan (default: current directory)",
    )
    parser.add_argument(
        "--pattern",
        default="*.txt",
        help="Glob pattern to match files (default: *.txt)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be saved without copying files",
    )

    args = parser.parse_args()

    if not args.path.exists() or not args.path.is_dir():
        print(f"❌ Error: {args.path} is not a valid directory", file=sys.stderr)
        return 2

    current_bag, saved_bag = fetch_needed_files(args.path, args.pattern)
    compute_diff(current_bag, saved_bag, args.path / "saves", dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
