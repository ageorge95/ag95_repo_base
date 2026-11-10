#!/usr/bin/env bash
# VERSION=2
# https://github.com/ageorge95/ag95_repo_base

pause() {
    if [ -t 0 ]; then
        echo ""
        read -r -p "Press Enter to exit..." _ || true
    fi
}

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

if ! source activate.sh; then
    echo "ERROR: could not activate the virtual environment. Run _install_templates/install.sh first." >&2
    pause
    exit 1
fi

python -m pip install --upgrade pyinstaller
pyinstaller main.spec
EXIT_CODE=$?

pause
exit $EXIT_CODE
