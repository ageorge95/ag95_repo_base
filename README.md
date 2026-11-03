# ag95_repo_base

Base skeleton for my Python GUI repositories. It contains the common files I
copy into a new project, plus the generic install/update scripts.

Each text file starts with a `VERSION=` line and the template repository URL.
Keep these lines when copying files, so you can see which template version was
used.

## What is included

| File | Purpose |
| --- | --- |
| `main.py` | Minimal PySide6 GUI entry point |
| `icon.ico` | Multi-size application/taskbar icon |
| `version.txt` | Version shown in the window title |
| `requirements.txt` | Python dependencies |
| `main.spec` | PyInstaller one-folder build definition |
| `BUILD_release.bat` | Builds the executable with PyInstaller |
| `START.bat` | Runs the app from the local virtual environment |
| `_install_templates/` | Generic install/update scripts (PowerShell and Bash) |

Package indexes used by the install/update scripts are configured in
`_install_templates/pip.ini`.

The install/update scripts use [uv](https://docs.astral.sh/uv/). If uv is
missing, they install it into `~/.local/bin` (PATH is not changed).

The allowed Python versions are set with `PYTHON_VERSION` (default
`'>=3.10,<3.14'`) in all four scripts; keep the value the same everywhere.
uv uses a matching Python that is already available. If none matches, uv
downloads the newest stable version inside the range, so the range's Python
does **not** have to be installed. `update.ps1` / `update.sh` stop if the
existing venv's Python is outside the range.

## Using this repo as a starting point

1. Create a new repository from this one (or copy the files).
2. Rename the app in `main.py` (`APP_NAME` and `APP_ID`) and, if needed, in `main.spec`.
3. Install the environment:
   - Windows: `powershell -ExecutionPolicy Bypass -File _install_templates\install.ps1`
   - Linux/macOS: `./_install_templates/install.sh`
   - Another Python version for one run: `install.ps1 -Python 3.11` / `install.sh --python 3.11`
4. Start the app with `START.bat` (Windows) or `python main.py`.
5. Update the environment later with `_install_templates\update.ps1` or
   `_install_templates/update.sh`.
6. Build a release with `BUILD_release.bat`; the output goes to `dist\main\`.

The install scripts work from the repository root or from a folder called
`_install` or `_install_templates`.
