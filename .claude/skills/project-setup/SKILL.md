---
name: project-setup
description: Sets up the project on a new machine by creating the Python virtual environment, installing the packages and downloading the Actual Burger database. Use before the first query of a session when `.venv/` or the `.duckdb` file in `data/` is missing, when a script fails because a package or the database is missing, or when the analyst asks to set up or reinstall the project.
---

# Project setup

Two things must exist before any query runs: a `.venv/` folder, and one `.duckdb` file in `data/`. Do only the steps for what's missing. Ask before each one, and wait for a yes.

Use the commands for the shell you're running in. Claude Code on Windows usually runs Git Bash: use forward slashes there, and the venv's Python is `.venv/Scripts/python.exe`.

## Step 1: Python packages

If there's no `.venv` folder, or a script fails because a package is missing, offer to create it and install the packages from `requirements.txt` (rerunning this on an existing `.venv` is safe):

- Mac/Linux: `python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt`
- Windows, Git Bash: `py -m venv .venv && .venv/Scripts/python.exe -m pip install -r requirements.txt`
- Windows, PowerShell: `py -m venv .venv; if ($LASTEXITCODE -eq 0) { .venv\Scripts\python.exe -m pip install -r requirements.txt }`

If Python isn't installed, or is older than 3.9 (check with `python3 --version`, or `py --version` on Windows), you can't fix that yourself: say so, and point the analyst to python.org.

## Step 2: The database

If there's no `.duckdb` file in `data/`, offer to download it. Say what it is: `actual_burger.zip`, about 90 MB (about 200 MB unzipped), from this project's GitHub releases. Download it, unzip it with the venv's Python (that works in every shell), and delete the zip:

- Mac/Linux: `curl -fL -o data/actual_burger.zip "https://github.com/actualinsight/actual-retail-analyst/releases/download/data-v1/actual_burger.zip" && .venv/bin/python -m zipfile -e data/actual_burger.zip data && rm data/actual_burger.zip`
- Windows, Git Bash: `curl -fL -o data/actual_burger.zip "https://github.com/actualinsight/actual-retail-analyst/releases/download/data-v1/actual_burger.zip" && .venv/Scripts/python.exe -m zipfile -e data/actual_burger.zip data && rm data/actual_burger.zip`
- Windows, PowerShell: `curl.exe -fL -o data\actual_burger.zip "https://github.com/actualinsight/actual-retail-analyst/releases/download/data-v1/actual_burger.zip"; if ($LASTEXITCODE -eq 0) { .venv\Scripts\python.exe -m zipfile -e data\actual_burger.zip data; Remove-Item data\actual_burger.zip }`

If the download fails, say so and stop: don't unzip a partial file, and delete any partial `data/actual_burger.zip` it left behind.

## Step 3: Confirm

Run one query to confirm the database opens (on Windows, use `.venv/Scripts/python.exe`):

```
.venv/bin/python .claude/skills/query-builder/query.py "SELECT COUNT(*) FROM store_dim"
```

Then carry on with what the analyst asked.
