@echo off
echo Starting ENT 101 Quiz Application...
python entrepreneurship_quiz_v2.py
if errorlevel 1 (
    echo.
    echo ERROR: Failed to run the quiz!
    echo Make sure you have run setup.bat first.
    pause
)
