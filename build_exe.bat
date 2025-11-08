@echo off
echo ===============================================
echo ENT 101 Quiz - Standalone EXE Builder
echo Created by Mehmet BARUK
echo ===============================================
echo.
echo Installing PyInstaller...
python -m pip install pyinstaller
echo.
echo Building standalone executable...
pyinstaller --onefile --windowed --name ENT101_Quiz --add-data "ENT 101 - Sample Midterm Questions.pdf;." --add-data "QuestionsExplanations.pdf;." --add-data "QuestionsExplanationsENG.pdf;." --add-data "QuestionsSourceMapping.pdf;." entrepreneurship_quiz_v2.py
echo.
echo Creating distribution folder...
if not exist distribution mkdir distribution
copy dist\ENT101_Quiz.exe distribution\
copy "ENT 101 - Sample Midterm Questions.pdf" distribution\
copy QuestionsExplanations.pdf distribution\
copy QuestionsExplanationsENG.pdf distribution\
copy QuestionsSourceMapping.pdf distribution\
echo.
echo ===============================================
echo Build complete!
echo ===============================================
echo.
echo The standalone executable is in: distribution\ENT101_Quiz.exe
echo.
pause
