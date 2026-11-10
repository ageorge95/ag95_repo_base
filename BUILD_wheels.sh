#!/usr/bin/env bash
# VERSION=1
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
    [ "$1" = "--no-pause" ] || pause
    exit 1
fi

python build_wheels.py
EXIT_CODE=$?

[ "$1" = "--no-pause" ] || pause
exit $EXIT_CODE
