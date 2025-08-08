# ChronoSave

ChronoSave is a lightweight, no-database Python tool for personal file versioning.  
It scans a folder, detects changes using SHA-256 hashing, and automatically saves versioned copies into a `saves/` directory.

No cloud dependency, no heavyweight setup — just run and keep your work safe.

---

## ✨ Features
- 📂 **Automatic change detection** — Hashes file contents to detect any modifications.
- 📝 **Versioned backups** — Saves changed files with incrementing suffixes like `draft__saved_001.txt`.
- ⚡ **Lightweight** — Single Python project, no daemon or service.
- 🎨 **Readable output** — Uses [Rich](https://github.com/Textualize/rich) tables for a pleasant CLI experience.
- 🛡 **Safe by default** — Keeps original files intact.

---

## 🚀 Installation

Clone the repo and install in editable mode so `chronosave` becomes a global command in your environment:

```bash
git clone https://github.com/YOUR_USERNAME/ChronoSave.git
cd ChronoSave

# (Optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install in editable mode
pip install -e .
```


## 💻 Usage
Basic usage (scan current directory):
```bash
chronosave .
```

Scan another folder:
```bash
chronosave .
```

Change the file pattern:
```bash
chronosave . --pattern "*.log"
```

Dry-run mode (show what would be saved without copying files):
```bash
chronosave . --dry-run
```

## 📌 Example Output:
```bash
📂 Scanning for files
────────────────────────────────────────────────────────────
base:        C:\Projects\ChronoSave
pattern:     *.txt
saves dir:   C:\Projects\ChronoSave\saves

┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name                 ┃ Hash         ┃ Last Updated         ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ draft_01_01_2025.txt │ d0f5e1cf9c68…│ 2025-08-01T15:42:42+02│
│ draft_01_05_2025.txt │ 23838aafa439…│ 2025-08-01T15:42:56+02│
└──────────────────────┴──────────────┴──────────────────────┘

🧮 Computing diff
────────────────────────────────────────────────────────────
dry_run:     False
saves_dir:   C:\Projects\ChronoSave\saves

✅ Nothing to save — everything up to date.
```

## Requirements
```bash
Python 3.10+
rich for pretty tables (installed automatically)
```


## Licence
MIT License — feel free to use and adapt.

















