@echo off
REM Check if Python is available
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python to run this script.
    exit /b 1
)

REM Check for required arguments
IF "%~1"=="" (
    echo Usage: convert.bat [notebook_path] [output_dir]
    exit /b 1
)

REM Set variables
SET NOTEBOOK_PATH=%~1
SET OUTPUT_DIR=%~2

REM Run the Markdown conversion
python markdown_converter.py %NOTEBOOK_PATH% %OUTPUT_DIR%

REM Handle success or failure
IF ERRORLEVEL 1 (
    echo Conversion failed.
    exit /b 1
) ELSE (
    echo Conversion successful.
)
