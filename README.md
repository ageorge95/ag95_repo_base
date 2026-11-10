# ag95_repo_base

Base skeleton for my Python GUI repositories. It contains the common files I
copy into a new project, plus the generic install/update scripts.

Each text file starts with a `VERSION=` line and the template repository URL.
Keep these lines when copying files, so you can see which template version was
used.

## What is included

| File | Purpose |
| --- | --- |
| `ag95_repo_base/main.py` | Minimal PySide6 GUI entry point |
| `ag95_repo_base/icon.ico` | Multi-size application/taskbar icon |
| `ag95_repo_base/version.txt` | Version shown in the window title; also the wheel version |
| `requirements.txt` | Python dependencies; also the wheel dependencies |
| `pyproject.toml` | Packaging metadata used to build the wheel |
| `main.spec` | PyInstaller one-folder build definition |
| `BUILD_release.bat` | Builds the executable with PyInstaller |
| `BUILD_wheels.bat` / `build_wheels.py` | Builds the wheel(s) with uv, optionally uploads them |
| `START.bat` | Runs the app from the local virtual environment |
| `_install_templates/` | Generic install/update scripts (PowerShell and Bash) |

Package indexes used by the install/update scripts are configured in
`_install_templates/pip.ini`.

The install/update scripts use [uv](https://docs.astral.sh/uv/). If uv is
missing, they install it into `~/.local/bin` (PATH is not changed); otherwise
they update it with `uv self update` (set `AUTO_UPDATE_UV` to `false` to turn
this off).

The allowed Python versions are set with `PYTHON_VERSION` (default
`'>=3.10,<3.14'`) in all four scripts; keep the value the same everywhere,
including `requires-python` in `pyproject.toml` and `PYTHON_VERSIONS` in
`build_wheels.py`.
uv uses a matching Python that is already available. If none matches, uv
downloads the newest stable version inside the range, so the range's Python
does **not** have to be installed. `update.ps1` / `update.sh` stop if the
existing venv's Python is outside the range.

## Using this repo as a starting point

1. Create a new repository from this one (or copy the files).
2. Rename the app in `ag95_repo_base/main.py` (`APP_NAME` and `APP_ID`).
   Rename the `ag95_repo_base` package folder and update every place that
   names it: `pyproject.toml`, `PACKAGE` in `main.spec` and `START.bat`.
3. Install the environment:
   - Windows: `powershell -ExecutionPolicy Bypass -File _install_templates\install.ps1`
   - Linux/macOS: `./_install_templates/install.sh`
   - Another Python version for one run: `install.ps1 -Python 3.11` / `install.sh --python 3.11`
4. Start the app with `START.bat` (Windows) or `python -m ag95_repo_base.main`.
5. Update the environment later with `_install_templates\update.ps1` or
   `_install_templates/update.sh`.
6. Build a release with `BUILD_release.bat`; the output goes to `dist\main\`.
7. Build the wheel with `BUILD_wheels.bat`; the output goes to `dist\wheels\`.

The install scripts work from the repository root or from a folder called
`_install` or `_install_templates`.

## Building wheels

`BUILD_wheels.bat` (or `python build_wheels.py`) builds the wheel described by
`pyproject.toml` with uv and writes it to `dist\wheels\`, next to the
PyInstaller output in `dist\main\`. The wheel version is read from
`ag95_repo_base/version.txt`, its dependencies from `requirements.txt`, and it
installs an `ag95-repo-base` GUI launcher. Pass `--no-pause` to
`BUILD_wheels.bat` to skip the final pause (CI).

uv is found on PATH or in `~/.local/bin` (where the install scripts put it).
It downloads any Python version it does not find, so the versions to build
with do **not** have to be installed. Package indexes come from `pip.ini`, like
in the install scripts.

Settings are at the top of `build_wheels.py`:

- `PURE_PYTHON_PACKAGE`: `True` builds one wheel with the newest version in
  `PYTHON_VERSIONS` (a pure Python wheel works with every Python version);
  `False` builds one wheel per version, which is needed for binary extensions.
- `PYPI_SERVER`: empty by default (build only). Set a server URL to upload the
  wheels with twine after the build. Credentials are read from the
  `TWINE_USERNAME` / `TWINE_PASSWORD` environment variables; twine asks for
  them if they are not set.

Before every build the script removes `dist\wheels`, `build` and `*.egg-info`,
so nothing stale ends up in a wheel. It fails if a wheel is empty or has
version `0.0.0`, which usually means a package name in `pyproject.toml` was not
updated after renaming the package folder.
