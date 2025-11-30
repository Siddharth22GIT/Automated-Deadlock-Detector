# Automated Deadlock Detector

A small Python project that simulates and detects deadlocks using a Wait-For Graph (WFG).

This repository includes both a command-line simulation and a simple Tkinter GUI for experimenting
with resource allocation, process requests/releases and deadlock detection.

## Features
- Simulation-driven deadlock detector (see `main.py`).
- GUI to interactively create processes and request/release resources (see `gui_app.py`).
- A lightweight deadlock detection engine that finds cycles in a Wait-For Graph (`deadlock_detector.py`).

## Quick start

Requirements: Python 3.8+ (no external dependencies are required by default).

This repository includes a `requirements.txt` at the project root. It is currently empty of runtime
dependencies because the project uses only Python's standard library. If third-party packages are added
in future, they will be listed in `requirements.txt` and can be installed with:

```powershell
pip install -r requirements.txt
```

From the project root you can run the simulation or start the GUI:

CLI simulation (sample run):

```powershell
python main.py
```

GUI:

```powershell
python gui_app.py
```

Notes:
- `setup.py` is included for packaging; you can use `pip install -e .` to install the package into your environment for development.

## Project layout

- `main.py` — example simulation runner that demonstrates process/resource interaction and deadlock detection.
- `gui_app.py` — simple Tkinter application to manually create processes and request/release resources.
- `resource_tracker.py` — tracks which process owns which resources.
- `process_monitor.py` — API for creating processes and requesting/releasing resources.
- `wfg_builder.py` — builds the Wait-For Graph used for deadlock detection.
- `deadlock_detector.py` — core detection logic (cycle detection in the WFG).
- `utils/` — helper modules such as `logger.py`.

## Caveats & notes
- Some files (e.g., `__main__.py`) may not be fully wired to the `main` entrypoint — running `main.py` directly works for the included simulation example.
- This repository contains example/demo code intended for experimentation and learning.

## Contributing
Feel free to open issues or PRs if you'd like this README expanded, a testsuite added, or the module packaging improved.

## License
Add a license file if you want to open-source the project; no license is included by default.
