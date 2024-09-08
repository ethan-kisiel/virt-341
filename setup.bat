@echo off
REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python to continue.
    exit /b 1
)

REM Create virtual environment in the 'env' folder
python -m venv env

REM Activate the virtual environment
call env\Scripts\activate

REM Check if the requirements.txt file exists
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found in the current directory.
)

echo Virtual environment setup complete.
pause