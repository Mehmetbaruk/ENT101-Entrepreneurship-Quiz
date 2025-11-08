"""
Batch Question Formatter for ENT 101 Quiz
This script helps you quickly format multiple questions at once.

USAGE:
1. Paste your questions below in SIMPLE FORMAT
2. Run this script: python batch_formatter.py
3. Copy the output and paste into entrepreneurship_quiz.py or entrepreneurship_quiz.html

SIMPLE FORMAT (pipe-separated):
ID|QUESTION|OPTION_A|OPTION_B|OPTION_C|OPTION_D|CORRECT_ANSWER|EXPLANATION

EXAMPLE:
3|What is entrepreneurship?|A business|A mindset|A process|All of the above|D|Entrepreneurship encompasses all these aspects.
4|Who is an entrepreneur?|A risk-taker|An innovator|A business owner|All of the above|D|Entrepreneurs embody all these characteristics.
"""

import sys

# Paste your questions here in simple format (one per line)
# Format: ID|QUESTION|A|B|C|D|CORRECT|EXPLANATION
SIMPLE_QUESTIONS = """
3|Entrepreneurship is the result of a disciplined, systematic process of applying ________ to needs and opportunities in the marketplace.|creativity and innovation|finance and economics|the political process|research and development|A|Entrepreneurship results from applying creativity and innovation to marketplace opportunities.
4|An entrepreneur is one who creates a new business in the face of ________ for the purpose of achieving profit and growth by identifying opportunities and assembling the necessary resources to capitalize on them.|risk and uncertainty|government regulations|competition|economic downturns|A|Entrepreneurs create businesses while facing risk and uncertainty, identifying and capitalizing on opportunities.
5|Research shows that most successful entrepreneurs possess certain characteristics including ________.|high energy level|desire for immediate feedback|future orientation|All of the above|D|Successful entrepreneurs typically possess high energy, desire immediate feedback, and are future-oriented, among other traits.
"""

def format_question_for_python(id_num, question, opt_a, opt_b, opt_c, opt_d, correct, explanation):
    """Format a question for Python code"""
    # Escape any quotes in the text
    question = question.replace('"', '\\"')
    opt_a = opt_a.replace('"', '\\"')
    opt_b = opt_b.replace('"', '\\"')
    opt_c = opt_c.replace('"', '\\"')
    opt_d = opt_d.replace('"', '\\"')
    explanation = explanation.replace('"', '\\"')
    
    return f'''    {{
        "id": {id_num},
        "question": "{question}",
        "options": {{
            "A": "{opt_a}",
            "B": "{opt_b}",
            "C": "{opt_c}",
            "D": "{opt_d}"
        }},
        "correct": "{correct}",
        "explanation": "{explanation}"
    }},'''

def format_question_for_javascript(id_num, question, opt_a, opt_b, opt_c, opt_d, correct, explanation):
    """Format a question for JavaScript/HTML code"""
    # Escape any quotes in the text
    question = question.replace("'", "\\'")
    opt_a = opt_a.replace("'", "\\'")
    opt_b = opt_b.replace("'", "\\'")
    opt_c = opt_c.replace("'", "\\'")
    opt_d = opt_d.replace("'", "\\'")
    explanation = explanation.replace("'", "\\'")
    
    return f'''            {{
                id: {id_num},
                question: '{question}',
                options: {{
                    A: '{opt_a}',
                    B: '{opt_b}',
                    C: '{opt_c}',
                    D: '{opt_d}'
                }},
                correct: '{correct}',
                explanation: '{explanation}'
            }},'''

def parse_and_format_questions(simple_text, output_format='python'):
    """Parse simple format questions and convert to code format"""
    questions = []
    errors = []
    
    for line_num, line in enumerate(simple_text.strip().split('\n'), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        parts = line.split('|')
        if len(parts) != 8:
            errors.append(f"Line {line_num}: Expected 8 parts, got {len(parts)}")
            continue
        
        try:
            id_num = int(parts[0].strip())
            question = parts[1].strip()
            opt_a = parts[2].strip()
            opt_b = parts[3].strip()
            opt_c = parts[4].strip()
            opt_d = parts[5].strip()
            correct = parts[6].strip().upper()
            explanation = parts[7].strip()
            
            if correct not in ['A', 'B', 'C', 'D']:
                errors.append(f"Line {line_num}: Invalid correct answer '{correct}' (must be A, B, C, or D)")
                continue
            
            if output_format == 'python':
                formatted = format_question_for_python(id_num, question, opt_a, opt_b, opt_c, opt_d, correct, explanation)
            else:
                formatted = format_question_for_javascript(id_num, question, opt_a, opt_b, opt_c, opt_d, correct, explanation)
            
            questions.append(formatted)
            
        except ValueError as e:
            errors.append(f"Line {line_num}: Error parsing - {str(e)}")
            continue
    
    return questions, errors

def main():
    print("=" * 80)
    print("ENT 101 BATCH QUESTION FORMATTER")
    print("=" * 80)
    print()
    
    if not SIMPLE_QUESTIONS.strip():
        print("⚠ No questions found!")
        print()
        print("Please paste your questions in SIMPLE FORMAT at the top of this script.")
        print("Format: ID|QUESTION|A|B|C|D|CORRECT|EXPLANATION")
        print()
        print("Example:")
        print("3|Question text?|Option A|Option B|Option C|Option D|A|Explanation here")
        return
    
    # Format for Python
    print("🐍 PYTHON FORMAT (for entrepreneurship_quiz.py):")
    print("-" * 80)
    python_questions, python_errors = parse_and_format_questions(SIMPLE_QUESTIONS, 'python')
    
    if python_errors:
        print("⚠ ERRORS FOUND:")
        for error in python_errors:
            print(f"  - {error}")
        print()
    
    if python_questions:
        print(f"✓ Successfully formatted {len(python_questions)} questions")
        print()
        print("Copy the following and paste it into entrepreneurship_quiz.py after question 2:")
        print()
        for q in python_questions:
            print(q)
    
    print()
    print("=" * 80)
    print()
    
    # Format for JavaScript
    print("🌐 JAVASCRIPT FORMAT (for entrepreneurship_quiz.html):")
    print("-" * 80)
    js_questions, js_errors = parse_and_format_questions(SIMPLE_QUESTIONS, 'javascript')
    
    if js_errors:
        print("⚠ ERRORS FOUND:")
        for error in js_errors:
            print(f"  - {error}")
        print()
    
    if js_questions:
        print(f"✓ Successfully formatted {len(js_questions)} questions")
        print()
        print("Copy the following and paste it into entrepreneurship_quiz.html after question 2:")
        print()
        for q in js_questions:
            print(q)
    
    print()
    print("=" * 80)
    print()
    print("📊 STATISTICS:")
    print(f"  - Questions processed: {len(python_questions)}")
    print(f"  - Errors encountered: {len(python_errors)}")
    print()
    print("💡 NEXT STEPS:")
    print("  1. Copy the formatted questions above")
    print("  2. Open entrepreneurship_quiz.py (for Python) or entrepreneurship_quiz.html (for web)")
    print("  3. Find the QUESTIONS array")
    print("  4. Paste the formatted questions after question 2")
    print("  5. Save the file")
    print("  6. Test the application!")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
    
    # Keep window open on Windows
    try:
        input("\nPress Enter to exit...")
    except:
        pass
