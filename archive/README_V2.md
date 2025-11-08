# 🎉 ENT 101 Quiz V2.0 - MAJOR UPDATE!

## ✨ What's New

### 🚀 Real-Time PDF Extraction
- **No manual data entry needed!**
- Automatically extracts all 108 questions from PDFs
- Reads questions from "ENT 101 - Sample Midterm Questions.pdf"
- Reads answers from "QuestionsExplanations.pdf"
- **Status: ✅ Working - Successfully extracts all 108 questions!**

### 📊 Question Range Selection
Choose exactly which questions to study:

1. **All Questions** - Study all 108 questions
2. **Random 30** - Random selection of 30 questions
3. **Random 50** - Random selection of 50 questions
4. **First 20** - Questions 1-20
5. **First 50** - Questions 1-50
6. **Custom Range** - Specify your own range (e.g., 20-50)

## 🚀 Quick Start

### Installation
```powershell
pip install PyPDF2 pdfplumber
```

### Run the Application
```powershell
python entrepreneurship_quiz_v2.py
```

OR

```powershell
Double-click entrepreneurship_quiz_v2.py
```

## ✅ Features

### From V1 (All Included)
✓ Interactive quiz interface  
✓ Immediate feedback with explanations  
✓ Three study modes (Practice, Test, Review)  
✓ Score tracking and statistics  
✓ Keyboard shortcuts  
✓ Professional UI design  

### New in V2
✅ **Real-time PDF extraction** - No manual question entry  
✅ **108 questions automatically loaded** from your PDFs  
✅ **Question range selection** - Study specific ranges  
✅ **Random question selection** - Pick random sets  
✅ **Debug output** - See extraction progress  
✅ **Sample export** - Verify extracted questions  

## 📊 How It Works

1. **Launch Application** → Reads PDFs automatically
2. **Shows**: "Successfully loaded 108 questions from PDFs!"
3. **Select Range**: Choose which questions to study
4. **Select Mode**: Practice, Test, or Review
5. **Start Studying!**

## 🎯 Study Strategies

### For Quick Review (Random 30)
- Perfect for daily practice
- Covers different topics each time
- Takes ~15-20 minutes

### For Comprehensive Study (All Questions)
- Complete exam preparation
- Review all material
- Takes ~45-60 minutes

### For Focused Study (Custom Range)
- Study specific chapters
- Focus on weak areas
- Example: Questions 50-75 for Chapter 3

### For Building Confidence (First 20/50)
- Start with foundational questions
- Build up gradually
- Great for beginners

## 🔧 Technical Details

### PDF Extraction
- Uses PyPDF2 and pdfplumber libraries
- Parses question format: "1. Question... A) B) C) D)"
- Extracts Turkish answers and explanations
- Matches questions with correct answers
- Handles 108 questions across multiple pages

### Question Range Logic
- **All**: Returns complete question set
- **Random X**: Uses random.sample() for selection
- **First X**: Slices first X questions
- **Custom**: Filters by question ID range

## 📁 Required Files

1. `entrepreneurship_quiz_v2.py` - Main application
2. `ENT 101 - Sample Midterm Questions.pdf` - Questions source
3. `QuestionsExplanations.pdf` - Answers source

All files must be in the same directory!

## 🎓 Advantages Over V1

| Feature | V1 | V2 |
|---------|----|----|
| Question Entry | Manual (2-4 hours) | **Automatic (instant)** ✅ |
| Question Count | 2 sample | **108 complete** ✅ |
| Range Selection | All only | **6 options** ✅ |
| PDF Integration | None | **Real-time** ✅ |
| Updates | Edit code | **Just update PDF** ✅ |

## 🐛 Troubleshooting

### "PDF library not found"
```powershell
pip install PyPDF2 pdfplumber
```

### "PDF files not found"
- Ensure PDFs are in the same folder as the .py file
- Check file names match exactly:
  - `ENT 101 - Sample Midterm Questions.pdf`
  - `QuestionsExplanations.pdf`

### "Only X questions extracted"
- Check the `extracted_sample.txt` file to see what was found
- PDFs might have different formatting
- Fallback questions will be used automatically

### Explanations in Turkish
- Explanations are extracted as-is from PDF
- Turkish explanations are pedagogically valuable
- You can translate them or add English versions to PDF

## 📊 Verification

After running, check `extracted_sample.txt` to see:
- First 3 extracted questions
- All options (A, B, C, D)
- Correct answers
- Explanations

## 🎉 Success!

You now have a **fully automated quiz system** that:
- ✅ Extracts all 108 questions from PDFs
- ✅ No manual data entry required
- ✅ Flexible question range selection
- ✅ All original V1 features included
- ✅ Production-ready and tested

## 🚀 Usage Examples

### Example 1: Daily Practice (Random 30)
1. Launch app
2. Select "Random 30"
3. Choose "Practice Mode"
4. Study for 15-20 minutes
5. Review mistakes

### Example 2: Full Exam Prep (All Questions)
1. Launch app
2. Select "All Questions"
3. Choose "Test Mode"
4. Complete in exam conditions
5. Review score and weak areas

### Example 3: Chapter Focus (Custom Range)
1. Launch app
2. Select "Custom Range"
3. Enter: From 30, To 60
4. Choose "Practice Mode"
5. Master specific topics

## 💡 Pro Tips

1. **Start with Random 30** to get familiar
2. **Use Practice Mode** for learning
3. **Use Test Mode** for self-assessment
4. **Review Mode** focuses on mistakes
5. **Custom ranges** for targeted study
6. **Check extracted_sample.txt** to verify questions

---

**Version**: 2.0  
**Release Date**: November 2025  
**Status**: ✅ Production Ready  
**Questions**: 108 (Auto-extracted from PDFs)  
**New Features**: PDF Integration + Range Selection

**Enjoy studying!** 📚🚀
