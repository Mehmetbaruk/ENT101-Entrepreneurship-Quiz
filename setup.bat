@echo off
echo ===============================================
echo ENT 101 Quiz Application - Setup
echo Created by Mehmet BARUK
echo ===============================================
echo.
echo Checking Python installation...
python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python found!
python --version
echo.
echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo ===============================================
echo Setup completed successfully!
echo ===============================================
echo.
echo To run the quiz: run_quiz.bat
echo.
pause
