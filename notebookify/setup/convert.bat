@echo off
REM Notebookify BAT Script for Repo

REM Path to Anaconda's activation script
set "CONDA_BAT=%~dp0..\..\..\anaconda3\Scripts\activate.bat"

REM Conda environment name
set "ENV_NAME=notebookify_env"

REM Relative path to the main script within the repo
set "SCRIPT_PATH=src\notebookify_main.py"

REM Debug variables (optional, can be removed for production)
echo CONDA_BAT: %CONDA_BAT%
echo ENV_NAME: %ENV_NAME%
echo SCRIPT_PATH: %SCRIPT_PATH%

REM Change directory to the repo's root (assumes .bat script is in the repo)
cd /d "%~dp0.."

REM Echo current directory for debugging
echo Current Directory: %cd%

REM Launch the script in a new terminal
start cmd /k "%CONDA_BAT% && conda activate %ENV_NAME% && python "%SCRIPT_PATH%" %* && conda deactivate && exit"
