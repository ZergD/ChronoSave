# ChronoSave

ChronoSave is a lightweight, no-database Python tool for personal file versioning.  
It watches your chosen folder, detects changes using SHA-256 hashing, and automatically saves versioned copies into a `saves/` directory.

No cloud dependency, no heavyweight setup — just run and keep your work safe.

---

## ✨ Features
- 📂 **Automatic change detection** — Hashes file contents to detect any modifications.
- 📝 **Versioned backups** — Saves changed files with incrementing suffixes like `draft__saved_001.txt`.
- ⚡ **Lightweight** — Single Python script, no daemon or service.
- 🎨 **Readable output** — Optional [Rich](https://github.com/Textualize/rich) tables for a pleasant CLI experience.
- 🛡 **Safe by default** — Keeps original files intact.

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ChronoSave.git
cd ChronoSave

# (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
python chronosave.py
