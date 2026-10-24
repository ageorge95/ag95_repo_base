# ag95_repo_base

Base skeleton for my Python GUI repositories. It contains the common files I
copy into a new project, plus the generic install/update scripts.

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

## Using this repo as a starting point

1. Create a new repository from this one (or copy the files).
2. Rename the app in `main.py` (`APP_NAME`) and, if needed, in `main.spec`.
3. Install the environment:
   - Windows: `powershell -ExecutionPolicy Bypass -File _install_templates\install.ps1`
   - Linux/macOS: `./_install_templates/install.sh`
4. Start the app with `START.bat` (Windows) or `python main.py`.
5. Update the environment later with `_install_templates\update.ps1` or
   `_install_templates/update.sh`.
6. Build a release with `BUILD_release.bat`; the output goes to `dist\main\`.

The install scripts work from the repository root or from a folder called
`_install` or `_install_templates`.
