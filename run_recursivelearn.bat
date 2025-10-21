@echo off
echo ========================================
echo  RecursiveLearn Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

echo Starting RecursiveLearn...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found.
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Could not create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Could not install dependencies
        pause
        exit /b 1
    )
)

REM Run the application
python main.py

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

echo.
echo RecursiveLearn closed.
pause
