"""
Question Extraction Helper Script
This script helps you manually add all 108 questions to the quiz application.

INSTRUCTIONS:
1. Open 'ENT 101 - Sample Midterm Questions.pdf' 
2. For each question (1-108), copy the text and paste it below
3. Open 'QuestionsExplanations.pdf'
4. Copy the corresponding explanation for each question
5. Format each question following the template below
6. Copy the formatted questions into entrepreneurship_quiz.py

QUESTION TEMPLATE:
{
    "id": 3,
    "question": "Your question text here?",
    "options": {
        "A": "First option",
        "B": "Second option",
        "C": "Third option",
        "D": "Fourth option"
    },
    "correct": "C",  # Replace with correct answer
    "explanation": "Detailed explanation of why this answer is correct."
},

CURRENT STATUS: 2 questions completed, 106 remaining

Below is space to add questions 3-108:
"""

# Add your questions below this line in the format shown above
# Questions 3-108 go here

ADDITIONAL_QUESTIONS = [
    # Question 3
    {
        "id": 3,
        "question": "[PASTE QUESTION 3 TEXT HERE]",
        "options": {
            "A": "[OPTION A]",
            "B": "[OPTION B]",
            "C": "[OPTION C]",
            "D": "[OPTION D]"
        },
        "correct": "[ANSWER]",
        "explanation": "[PASTE EXPLANATION HERE]"
    },
    # Continue adding questions 4-108 following the same format
    # You can copy this template for each question
]

# QUICK REFERENCE FOR TURKISH TO ENGLISH TRANSLATIONS (from QuestionsExplanations.pdf):
# Çözüm/Dayanak = Solution/Explanation
# Soru No = Question Number
# Cevap = Answer

print("""
================================================================================
ENT 101 QUESTION EXTRACTION HELPER
================================================================================

TO ADD ALL 108 QUESTIONS:

STEP 1: Extract Questions
--------------------------
1. Open 'ENT 101 - Sample Midterm Questions.pdf'
2. Copy questions 3-108 (questions 1-2 are already in the main file)
3. For each question, note:
   - Question number
   - Question text
   - Options A, B, C, D
   
STEP 2: Extract Answers & Explanations
---------------------------------------
1. Open 'QuestionsExplanations.pdf'
2. Find the answer for each question (in 'Cevap' column)
3. Copy the explanation (in 'Çözüm/Dayanak' column)
4. Translate Turkish explanations to English if needed

STEP 3: Format Questions
-------------------------
Use this template for each question:

    {
        "id": X,
        "question": "Question text here?",
        "options": {
            "A": "Option A text",
            "B": "Option B text",
            "C": "Option C text",
            "D": "Option D text"
        },
        "correct": "A",
        "explanation": "Explanation text here."
    },

STEP 4: Add to Main File
-------------------------
1. Open 'entrepreneurship_quiz.py'
2. Find the QUESTIONS list (around line 22)
3. Add all formatted questions after question 2
4. Save the file

STEP 5: Test
------------
Run: python entrepreneurship_quiz.py
Verify all 108 questions load correctly

================================================================================
TIPS:
- Use a text editor with find/replace to speed up formatting
- Keep explanations concise but informative
- Ensure all special characters are properly encoded
- Test the quiz after adding every 10-20 questions
================================================================================
""")

# Optional: If you want to provide questions in a simpler format, use this:
# Format: ID|QUESTION|A|B|C|D|CORRECT|EXPLANATION
SIMPLE_FORMAT_EXAMPLE = """
3|Question text here?|Option A|Option B|Option C|Option D|C|Explanation here
4|Next question?|Option A|Option B|Option C|Option D|A|Explanation here
"""

# You can paste questions in simple format above, then run this script
# It will convert them to the proper Python dictionary format

def parse_simple_format(simple_text):
    """Convert simple format to Python dictionary format"""
    questions = []
    for line in simple_text.strip().split('\n'):
        if not line.strip() or line.startswith('#'):
            continue
        parts = line.split('|')
        if len(parts) == 8:
            question = {
                "id": int(parts[0]),
                "question": parts[1],
                "options": {
                    "A": parts[2],
                    "B": parts[3],
                    "C": parts[4],
                    "D": parts[5]
                },
                "correct": parts[6],
                "explanation": parts[7]
            }
            questions.append(question)
    return questions

# To use the converter, paste your questions in SIMPLE_FORMAT_EXAMPLE above
# Then uncomment the lines below:

# converted = parse_simple_format(SIMPLE_FORMAT_EXAMPLE)
# for q in converted:
#     print(f"    {q},")
