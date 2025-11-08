#!/usr/bin/env python3
"""
Debug script to see what's in the PDFs
"""

try:
    import PyPDF2
    
    # Check questions PDF
    print("=" * 80)
    print("QUESTIONS PDF Analysis")
    print("=" * 80)
    
    with open("ENT 101 - Sample Midterm Questions.pdf", 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        print(f"Total pages: {len(reader.pages)}")
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            print(f"\n--- Page {i+1} ({len(text)} chars) ---")
            # Show first 500 characters
            print(text[:500])
            print("...")
            # Count question numbers on this page
            import re
            questions = re.findall(r'\b(\d+)\.\s+', text)
            print(f"Question numbers found: {questions[:10]}")
    
    print("\n" + "=" * 80)
    print("ANSWERS PDF Analysis")
    print("=" * 80)
    
    with open("QuestionsExplanations.pdf", 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        print(f"Total pages: {len(reader.pages)}")
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            print(f"\n--- Page {i+1} ({len(text)} chars) ---")
            print(text[:500])
            print("...")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
