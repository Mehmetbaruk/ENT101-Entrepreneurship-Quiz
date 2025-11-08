# ENT 101 Entrepreneurship Quiz Application

**Created by Mehmet BARUK, Computer Engineering**  
LinkedIn: [in/mehmet-baruk](https://linkedin.com/in/mehmet-baruk/)

## Overview
A comprehensive interactive quiz application for ENT 101 Entrepreneurship course with 108 multiple-choice questions, bilingual explanations, and detailed source mapping.

## Key Features
- **108 Questions**: Auto-extracted from official midterm PDF
- **Bilingual Support**: Toggle between Turkish and English explanations
- **Source Mapping**: View chapter, topic, and reference information for each question
- **Responsive UI**: Scrollable interface that adapts to any window size
- **3 Study Modes**: Practice, Timed Test, Review All
- **6 Question Ranges**: All Questions, 1-36, 37-72, 73-108, Random 36, Custom Range
- **Smart Navigation**: Jump to any question instantly
- **Progress Tracking**: Real-time score and answer tracking

## Installation Methods

### Option 1: Run with Python (Recommended for Development)
1. Run setup.bat to install dependencies
2. Run un_quiz.bat to start the application

### Option 2: Standalone Executable (No Python Required)
1. Run uild_exe.bat to create standalone EXE
2. Find ENT101_Quiz.exe in the distribution folder
3. Share the entire distribution folder with students

### Option 3: Manual Setup
`powershell
# Install Python 3.7+
python -m pip install PyPDF2>=3.0.0
python entrepreneurship_quiz_v2.py
`

## Requirements
- Python 3.7+ (not needed for standalone EXE)
- PyPDF2 library
- 4 PDF files (included):
  - ENT 101 - Sample Midterm Questions.pdf
  - QuestionsExplanations.pdf
  - QuestionsExplanationsENG.pdf
  - QuestionsSourceMapping.pdf

## Usage
1. Select study mode (Practice/Timed/Review)
2. Choose question range
3. Answer questions and navigate using buttons
4. Toggle explanation language with "Show Turkish/English" button
5. View source mapping for additional context
6. Submit quiz to see your score

## File Structure
`
ENT101_Entrepreneurship_Girisimcilik_Midterm/
├── entrepreneurship_quiz_v2.py  # Main application
├── setup.bat                     # Auto-install dependencies
├── run_quiz.bat                  # Launch application
├── build_exe.bat                 # Build standalone EXE
├── requirements.txt              # Python dependencies
├── LICENSE                       # MIT License
├── README.md                     # This file
├── QUICK_START.md                # User guide
├── *.pdf                         # Question and explanation PDFs
└── archive/                      # Old/unused files
`

## Troubleshooting
- **Python not found**: Install from [python.org](https://www.python.org/downloads/)
- **PDF not found**: Keep all 4 PDF files in the same folder as the application
- **Import error**: Run setup.bat or python -m pip install PyPDF2
- **Questions not loading**: Ensure PDF files are not corrupted

## Credits
Developed by **Mehmet BARUK**  
Computer Engineering Student  
LinkedIn: [in/mehmet-baruk](https://linkedin.com/in/mehmet-baruk/)

## License
MIT License - See LICENSE file for details
