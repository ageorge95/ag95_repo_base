@echo off
REM VERSION=1
REM https://github.com/ageorge95/ag95_repo_base

call activate.bat
python build_wheels.py
set EXIT_CODE=%ERRORLEVEL%
if /i not "%~1"=="--no-pause" pause
exit /b %EXIT_CODE%
