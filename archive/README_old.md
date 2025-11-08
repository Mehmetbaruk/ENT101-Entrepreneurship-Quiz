# ENT 101 Entrepreneurship Interactive Quiz Application

A comprehensive, production-ready quiz system designed for ENT 101 Entrepreneurship students.

## 🚀 Quick Start

### Windows
1. Double-click `entrepreneurship_quiz.py`
   OR
2. Open PowerShell/Command Prompt in this folder and run:
   ```
   python entrepreneurship_quiz.py
   ```

### Mac/Linux
1. Open Terminal in this folder and run:
   ```
   python3 entrepreneurship_quiz.py
   ```

## 📋 System Requirements

- **Python**: Version 3.6 or higher (pre-installed on Mac/Linux, downloadable for Windows from python.org)
- **Libraries**: Only uses Python standard library (Tkinter) - no additional installations needed
- **OS**: Windows 7+, macOS 10.12+, Linux (any recent distribution)
- **RAM**: 256 MB minimum
- **Screen Resolution**: 1024x768 or higher recommended

## ✨ Features

### 🎯 Study Modes

1. **Practice Mode**
   - See correct answers immediately after submission
   - Detailed explanations for each question
   - Perfect for learning and understanding concepts
   - Real-time score tracking

2. **Test Mode**
   - Simulates real exam conditions
   - See all results at the end
   - No immediate feedback during quiz
   - Ideal for self-assessment

3. **Review Mode**
   - Focus on previously missed questions
   - Available after completing Practice or Test mode
   - Reinforces weak areas
   - Track your improvement

### 📊 Smart Features

- ✅ **Immediate Feedback**: Color-coded answers (green = correct, red = incorrect)
- 📚 **Detailed Explanations**: Learn why each answer is correct
- 🔀 **Question Randomization**: Different order each session
- 📈 **Score Tracking**: Real-time accuracy percentage
- ⏱ **Time Tracking**: Monitor how long you spend studying
- ⌨ **Keyboard Shortcuts**: 
  - `Enter` = Submit answer / Next question
  - `Arrow Keys` = Navigate
  - `Esc` = Back to menu
- 💾 **Progress Indicator**: Always know where you are (Question X/108)
- 🎨 **Professional UI**: Clean, academic design optimized for studying

### 📱 User Interface

- Clean, modern design with professional color scheme
- Large, readable fonts (minimum 12pt)
- Proper spacing for comfortable reading
- Intuitive navigation
- No technical knowledge required

## 📚 Question Database

- **Total Questions**: 108 comprehensive entrepreneurship questions
- **Format**: Multiple choice (A, B, C, D)
- **Coverage**: Complete ENT 101 midterm syllabus
- **Quality**: Each question includes detailed explanations

## 🎓 How to Use

### Starting a Quiz

1. **Launch the application**
2. **Select your study mode**:
   - Choose Practice Mode for learning
   - Choose Test Mode for assessment
   - Choose Review Mode to focus on mistakes
3. **Answer questions**:
   - Click on your chosen answer
   - Press Submit or hit Enter
   - Read the explanation (in Practice/Review modes)
   - Click Next or press Enter to continue
4. **View Results**:
   - See your final score and percentage
   - Review time taken
   - Option to retry or review missed questions

### Tips for Best Results

- 📖 **Start with Practice Mode** to learn the material
- 🧪 **Use Test Mode** when you feel confident
- 🔍 **Review Mode** helps reinforce weak areas
- 📝 **Take notes** on explanations for difficult questions
- 🔄 **Repeat** until you consistently score above 80%
- ⏰ **Time yourself** to simulate exam conditions

## 🛠 Troubleshooting

### "Python is not recognized" error
- Install Python from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"

### Tkinter not found error
- **Windows**: Reinstall Python with "tcl/tk and IDLE" option checked
- **Linux**: Run `sudo apt-get install python3-tk`
- **Mac**: Tkinter comes pre-installed with Python

### Application won't start
1. Verify Python version: `python --version` (should be 3.6+)
2. Try: `python3 entrepreneurship_quiz.py` instead
3. Check file permissions (should be readable)

### Display issues
- Increase window size if content appears cramped
- Minimum screen resolution: 1024x768
- Try adjusting system display scaling if text is too small/large

## 📊 Performance Metrics

- **90-100%**: Outstanding - You're well-prepared! 🌟
- **80-89%**: Excellent - Minor review needed 👏
- **70-79%**: Good - Keep practicing 👍
- **60-69%**: Fair - More study recommended 📚
- **Below 60%**: Needs work - Focus on weak areas 💪

## 🔄 Updating Questions

To add or modify questions, edit the `QUESTIONS` list in `entrepreneurship_quiz.py`:

```python
{
    "id": 109,  # Unique ID
    "question": "Your question text here?",
    "options": {
        "A": "Option A text",
        "B": "Option B text",
        "C": "Option C text",
        "D": "Option D text"
    },
    "correct": "A",  # The correct answer (A, B, C, or D)
    "explanation": "Detailed explanation of why this answer is correct."
}
```

## 📄 Project Structure

```
ENT101_Entrepreneurship_Girisimcilik_Midterm/
│
├── entrepreneurship_quiz.py    # Main application (single file)
├── README.md                   # This file
├── ENT 101 - Sample Midterm Questions.pdf
└── QuestionsExplanations.pdf
```

## 🎯 Success Criteria

This application meets all project requirements:

✅ Fully interactive GUI with Tkinter  
✅ All 108 questions with correct answers  
✅ Detailed explanations for each question  
✅ Multiple study modes (Practice, Test, Review)  
✅ Real-time score tracking and feedback  
✅ Question randomization  
✅ Professional, academic UI design  
✅ Keyboard shortcuts for efficiency  
✅ Progress indicators and time tracking  
✅ Review incorrect questions feature  
✅ Single file, no external dependencies  
✅ Cross-platform compatibility  
✅ Immediate execution without setup  

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify all system requirements are met
3. Ensure Python 3.6+ is properly installed
4. Try running from command line to see error messages

## 📝 License

This educational software is created for ENT 101 Entrepreneurship course students.

## 🎓 Good Luck!

Study hard, practice regularly, and ace that midterm! 🌟

---
**Version**: 1.0  
**Last Updated**: November 2025  
**Questions**: 108  
**Supported Platforms**: Windows, macOS, Linux
