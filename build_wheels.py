# VERSION=1
# https://github.com/ageorge95/ag95_repo_base

"""Build the wheel(s) of this repository with uv and optionally upload them.

Run it with BUILD_wheels.bat (activates the virtual environment first) or with
'python build_wheels.py'. Only the standard library and uv are needed; uv
downloads any Python version that is not installed. uv is found on PATH or in
the folder the install scripts put it in.
"""

import configparser
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

# True : the package is pure Python, so a single wheel built with the first
#        (newest) version in PYTHON_VERSIONS is compatible with every Python version.
# False: the package has binary extensions, so one wheel is built for every
#        version in PYTHON_VERSIONS.
PURE_PYTHON_PACKAGE = True

# Python versions to build with, newest first. Keep them inside the allowed
# range ('requires-python' in pyproject.toml, PYTHON_VERSION in the install scripts).
PYTHON_VERSIONS = ['3.15', '3.14', '3.13', '3.12', '3.11', '3.10']

# Where the wheels are written, relative to the repository root. Separate from
# dist\main (BUILD_release.bat) and wiped before every build.
OUTPUT_DIR = Path('dist') / 'wheels'

# Package server the wheels are uploaded to with twine after a successful
# build, e.g. 'http://my-server.example.com:8080/'. Empty = build only.
# Credentials come from the TWINE_USERNAME / TWINE_PASSWORD environment
# variables; twine asks for them if they are not set.
PYPI_SERVER = ''

# Package index configuration, the same file the install scripts use. It is
# looked up in these folders (relative to the repository root), in order, and
# is used to download the build tools (and twine).
PIP_CONFIG = 'pip.ini'
PIP_CONFIG_DIRS = ['_install', '_install_templates', '.']

# ============================================================
# HELPERS (no changes needed below this line)
# ============================================================

REPO_ROOT = Path(__file__).resolve().parent


def find_uv():
    """Return the path of an existing uv executable, or None."""
    uv = shutil.which('uv')
    if uv:
        return uv
    for folder in (Path.home() / '.local' / 'bin', Path.home() / '.cargo' / 'bin'):
        for name in ('uv.exe', 'uv'):
            if (folder / name).is_file():
                return str(folder / name)
    return None


def read_index_args():
    """Return the uv options matching the index settings of the pip config."""
    for folder in PIP_CONFIG_DIRS:
        config_path = REPO_ROOT / folder / PIP_CONFIG
        if config_path.is_file():
            break
    else:
        print(f"'{PIP_CONFIG}' not found, using the default package index of uv.")
        return []

    parser = configparser.ConfigParser(strict=False, interpolation=None)
    parser.read(config_path, encoding='utf-8')
    values = {'index-url': [], 'extra-index-url': [], 'trusted-host': []}
    for section in parser.sections():
        for key, value in parser.items(section):
            name = key.lower().replace('_', '-')
            if name in values:
                values[name] += value.split()

    args = []
    if values['index-url']:
        args += ['--index-url', values['index-url'][0]]
    for url in values['extra-index-url']:
        args += ['--extra-index-url', url]
    for host in values['trusted-host']:
        args += ['--allow-insecure-host', host]
    # Like pip: pick the best matching version across all indexes.
    if values['extra-index-url']:
        args += ['--index-strategy', 'unsafe-best-match']
    return args


def run(command):
    command = [str(part) for part in command]
    print(f"> {' '.join(command)}")
    subprocess.run(command, check=True)


def clean():
    """Remove the output of earlier builds, so nothing stale ends up in a wheel."""
    for path in [OUTPUT_DIR, Path('build'), *Path('.').glob('*.egg-info')]:
        if path.is_dir():
            print(f'Removing {path}')
            shutil.rmtree(path)


def build_wheel(uv, python_version, index_args):
    print(f'\n==> Building the wheel with Python {python_version}...')
    run([uv, 'build', '--wheel',
         '--python', python_version,
         '--out-dir', OUTPUT_DIR,
         '--no-create-gitignore',
         *index_args])


def check_wheel(wheel):
    """Catch packaging mistakes that setuptools silently accepts."""
    with zipfile.ZipFile(wheel) as archive:
        files = [name for name in archive.namelist() if '.dist-info/' not in name]
    if not files:
        raise ValueError(f'{wheel.name} is empty, check the package settings in pyproject.toml.')
    if wheel.name.split('-')[1] == '0.0.0':
        raise ValueError(f'{wheel.name} has version 0.0.0, check the version settings in pyproject.toml.')


def upload_wheels(uv, wheels, index_args):
    print(f'\n==> Uploading the wheels to {PYPI_SERVER}...')
    run([uv, 'tool', 'run', *index_args,
         'twine', 'upload', '--repository-url', PYPI_SERVER,
         *wheels])


def main():
    # Keep our output in order with uv's when stdout is redirected (CI, logs).
    sys.stdout.reconfigure(line_buffering=True)
    os.chdir(REPO_ROOT)

    uv = find_uv()
    if not uv:
        print('ERROR: uv was not found. Run the install script first (it installs uv) '
              'or install it from https://docs.astral.sh/uv/getting-started/installation/',
              file=sys.stderr)
        return 1
    print(f'Using {uv}')

    index_args = read_index_args()
    python_versions = PYTHON_VERSIONS[:1] if PURE_PYTHON_PACKAGE else PYTHON_VERSIONS

    try:
        print()
        clean()
        for python_version in python_versions:
            build_wheel(uv, python_version, index_args)

        wheels = sorted(OUTPUT_DIR.glob('*.whl'))
        if not wheels:
            raise ValueError(f'no wheel was found in {OUTPUT_DIR}.')
        print('\nWheels built:')
        for wheel in wheels:
            check_wheel(wheel)
            print(f'  {wheel}')

        if PYPI_SERVER:
            upload_wheels(uv, wheels, index_args)
    except (subprocess.CalledProcessError, ValueError) as error:
        print(f'\nERROR: {error}', file=sys.stderr)
        print('\n!!!!! BUILD FAILED !!!!!', file=sys.stderr)
        return 1

    print('\nBuild complete.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
