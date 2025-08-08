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
chronosave .

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

## Example with pattern and dry run to see the potential result:
Dry run means, it didn't do the copy but just shows what would happen:
```bash
chronosave . --pattern "*.log" --dry-run

INFO
INFO     📂 Scanning for files
INFO     ————————————————————————————————————————————————————————————
INFO     base: /Users/user/Documents/drafts_perso_txt
INFO     pattern: *.log
INFO     saves dir: /Users/user/Documents/drafts_perso_txt/saves

                            Current files
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ last_updated                     ┃ hash8    ┃ name     ┃ path     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ 2025-08-08T19:43:18.436727+02:00 │ bd51c924 │ run.log  │ run.log  │
│ 2025-08-08T19:42:56.289287+02:00 │ 9781765b │ test.log │ test.log │
└──────────────────────────────────┴──────────┴──────────┴──────────┘
INFO
INFO     🗒️ Saved files (empty)
INFO     ————————————————————————————————————————————————————————————
INFO
INFO     🧮 Computing diff
INFO     ————————————————————————————————————————————————————————————
INFO     dry_run: True
INFO     saves_dir: /Users/user/Documents/drafts_perso_txt/saves
INFO
INFO     ✅ New saves created
INFO     ————————————————————————————————————————————————————————————
           Created
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ target                    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ saves/run__saved_001.log  │
│ saves/test__saved_001.log │
└───────────────────────────┘
```

## Requirements
```bash
Python 3.10+
rich for pretty tables (installed automatically)
```


## Licence
MIT License — feel free to use and adapt.

















