#!/usr/bin/env python3
"""
ENT 101 Entrepreneurship Interactive Quiz Application V2
With Real-Time PDF Extraction and Question Range Selection
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from datetime import datetime
from typing import List, Dict, Optional
import re
import os

# Try to import PDF libraries
try:
    import PyPDF2
    PDF_LIBRARY = 'PyPDF2'
except ImportError:
    try:
        import pdfplumber
        PDF_LIBRARY = 'pdfplumber'
    except ImportError:
        PDF_LIBRARY = None

# ==================== PDF EXTRACTION ====================
class PDFQuestionExtractor:
    """Extract questions and answers from PDF files"""
    
    def __init__(self, questions_pdf: str, answers_turkish_pdf: str, answers_english_pdf: str, source_mapping_pdf: str = ""):
        self.questions_pdf = questions_pdf
        self.answers_turkish_pdf = answers_turkish_pdf
        self.answers_english_pdf = answers_english_pdf
        self.source_mapping_pdf = source_mapping_pdf
        self.questions = []
        
    def extract_with_pypdf2(self, pdf_path: str) -> str:
        """Extract text using PyPDF2"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"PyPDF2 extraction error: {e}")
        return text
    
    def extract_with_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber"""
        text = ""
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"pdfplumber extraction error: {e}")
        return text
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using available library"""
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            return ""
        
        if PDF_LIBRARY == 'PyPDF2':
            return self.extract_with_pypdf2(pdf_path)
        elif PDF_LIBRARY == 'pdfplumber':
            return self.extract_with_pdfplumber(pdf_path)
        else:
            print("No PDF library available. Please install: pip install PyPDF2 pdfplumber")
            return ""
    
    def parse_questions(self, text: str) -> List[Dict]:
        """Parse questions from extracted text"""
        questions = []
        
        # Clean up text - remove extra spaces and normalize
        text = re.sub(r'\s+', ' ', text)
        
        # Split by question numbers (1. 2. 3. etc.)
        # Look for patterns like "1. " or "1." at start or after newline
        question_blocks = re.split(r'\s(\d+)\.\s+', text)
        
        # Process blocks (odd indices are question numbers, even are content)
        for i in range(1, len(question_blocks), 2):
            if i+1 >= len(question_blocks):
                break
                
            q_num = int(question_blocks[i])
            content = question_blocks[i+1].strip()
            
            # Find where options start (look for "A)")
            options_start = content.find('A)')
            if options_start == -1:
                continue
            
            # Extract question text
            question_text = content[:options_start].strip()
            
            # Extract options
            options_text = content[options_start:]
            
            # Parse each option
            options = {}
            for opt_letter in ['A', 'B', 'C', 'D']:
                pattern = rf'{opt_letter}\)(.*?)(?=[B-D]\)|$)'
                match = re.search(pattern, options_text, re.DOTALL)
                if match:
                    option_text = match.group(1).strip()
                    # Clean up option text - remove extra spaces
                    option_text = re.sub(r'\s+', ' ', option_text)
                    options[opt_letter] = option_text
            
            # Only add if we have all 4 options
            if len(options) == 4 and question_text:
                questions.append({
                    'id': q_num,
                    'question': question_text,
                    'options': options
                })
        
        return questions
    
    def parse_answers(self, text: str) -> Dict[int, Dict]:
        """Parse answers and explanations from extracted text (single language)"""
        answers = {}
        
        # Clean text
        text = re.sub(r'\s+', ' ', text)
        
        # Pattern: Table format with pipes | Soru No | Cevap | Çözüm/Dayanak |
        table_pattern = r'\|\s*\*?\*?(\d+)\.\*?\*?\s*\|\s*\*?\*?([A-D])\*?\*?\s*\|\s*([^|]+)'
        matches = re.finditer(table_pattern, text)
        
        for match in matches:
            q_num = int(match.group(1))
            answer = match.group(2).strip()
            explanation = match.group(3).strip()
            
            # Clean explanation
            explanation = re.sub(r'\*+', '', explanation)
            explanation = re.sub(r'\s+', ' ', explanation)
            
            # Ensure minimum length
            if len(explanation) < 15:
                explanation = f"Correct answer: {answer}. " + explanation
            
            answers[q_num] = {
                'correct': answer,
                'explanation': explanation
            }
        
        # Pattern 2: Simple format - if table parsing didn't work well
        if len(answers) < 10:
            simple_pattern = r'(\d+)[^\w]+([A-D])(?:\s|\|)+'
            matches = re.finditer(simple_pattern, text)
            for match in matches:
                q_num = int(match.group(1))
                answer = match.group(2).strip()
                
                if q_num not in answers:
                    # Try to find explanation after the answer
                    start_pos = match.end()
                    end_pos = text.find(str(q_num + 1), start_pos)
                    if end_pos == -1:
                        end_pos = start_pos + 500
                    
                    explanation = text[start_pos:end_pos].strip()
                    explanation = re.sub(r'\|+', '', explanation)
                    explanation = re.sub(r'\*+', '', explanation)
                    explanation = re.sub(r'\s+', ' ', explanation)
                    
                    # Try to detect English/Turkish split
                    turkish_exp = explanation
                    english_exp = explanation
                    
                    if len(explanation) < 15:
                        turkish_exp = f"Doğru cevap {answer}. Girişimcilik ilkelerine dayanmaktadır."
                        english_exp = f"The correct answer is {answer} based on entrepreneurship principles."
                    
                    answers[q_num] = {
                        'correct': answer,
                        'explanation_turkish': turkish_exp[:500],
                        'explanation_english': english_exp[:500]
                    }
        
        return answers
    
    def parse_source_mapping(self, text: str) -> Dict[int, Dict]:
        """Parse source mapping from the source PDF"""
        sources = {}
        
        # Clean text but preserve structure
        text = re.sub(r'\s+', ' ', text)
        
        # Extract chapter sections
        # Pattern: ## QUESTIONS X-Y: Chapter N - Title (with flexible spacing)
        chapter_pattern = r'## QUESTIONS\s*(\d+)\s*-\s*(\d+)\s*:\s*(Chapter\s+\d+[^|#]+)'
        chapters = list(re.finditer(chapter_pattern, text, re.IGNORECASE))
        
        print(f"   Found {len(chapters)} chapter sections")
        
        for i, chapter_match in enumerate(chapters):
            start_q = int(chapter_match.group(1))
            end_q = int(chapter_match.group(2))
            chapter_title = chapter_match.group(3).strip()
            
            print(f"   Chapter: {chapter_title} (Q{start_q}-{end_q})")
            
            # Find the section of text for this chapter
            chapter_start = chapter_match.end()
            if i + 1 < len(chapters):
                chapter_end = chapters[i + 1].start()
            else:
                chapter_end = len(text)
            
            chapter_text = text[chapter_start:chapter_end]
            
            # Parse individual question mappings within this chapter
            # Pattern: | 1 | Topic | Source Reference |
            row_pattern = r'\|\s*(\d+)\s*\|([^|]+)\|([^|]+)'
            rows = re.finditer(row_pattern, chapter_text)
            
            for row in rows:
                q_num = int(row.group(1))
                topic = row.group(2).strip()
                source_ref = row.group(3).strip()
                
                # Skip header rows
                if 'Question' in topic or 'Topic' in topic:
                    continue
                
                # Extract document name if present
                doc_match = re.search(r'(ENT\s+101[^"|]+\.pdf)', source_ref, re.IGNORECASE)
                ref_match = re.search(r'\[\[(\d+)\]\]', source_ref)
                
                sources[q_num] = {
                    'source': source_ref,
                    'source_chapter': chapter_title,
                    'source_document': doc_match.group(1).strip() if doc_match else f"{chapter_title}.pdf",
                    'source_reference': ref_match.group(0) if ref_match else "",
                    'topic': topic
                }
        
        print(f"   Parsed {len(sources)} question sources")
        return sources
    
    def extract_all_questions(self) -> List[Dict]:
        """Extract and combine questions with answers from both language PDFs"""
        print("=" * 80)
        print("Starting PDF Extraction...")
        print("=" * 80)
        
        # Extract text from questions PDF
        print(f"\n1. Extracting from: {self.questions_pdf}")
        questions_text = self.extract_text_from_pdf(self.questions_pdf)
        print(f"   Extracted {len(questions_text)} characters")
        
        # Extract text from Turkish explanations PDF
        print(f"\n2. Extracting from: {self.answers_turkish_pdf}")
        answers_turkish_text = self.extract_text_from_pdf(self.answers_turkish_pdf)
        print(f"   Extracted {len(answers_turkish_text)} characters")
        
        # Extract text from English explanations PDF
        print(f"\n3. Extracting from: {self.answers_english_pdf}")
        answers_english_text = self.extract_text_from_pdf(self.answers_english_pdf)
        print(f"   Extracted {len(answers_english_text)} characters")
        
        if not questions_text:
            print("\n❌ Failed to extract questions from PDF")
            return self.get_fallback_questions()
        
        # Parse questions
        print("\n4. Parsing questions...")
        questions = self.parse_questions(questions_text)
        print(f"   ✓ Extracted {len(questions)} questions")
        
        if len(questions) > 0:
            print(f"   Sample: Q{questions[0]['id']}: {questions[0]['question'][:50]}...")
        
        # Parse Turkish answers and explanations
        print("\n5. Parsing Turkish answers and explanations...")
        answers_turkish = self.parse_answers(answers_turkish_text)
        print(f"   ✓ Extracted {len(answers_turkish)} Turkish answers")
        
        # Parse English answers and explanations
        print("\n6. Parsing English answers and explanations...")
        answers_english = self.parse_answers(answers_english_text)
        print(f"   ✓ Extracted {len(answers_english)} English answers")
        
        # Parse source mapping if available
        sources = {}
        if self.source_mapping_pdf and os.path.exists(self.source_mapping_pdf):
            print(f"\n7. Extracting from: {self.source_mapping_pdf}")
            source_text = self.extract_text_from_pdf(self.source_mapping_pdf)
            print(f"   Extracted {len(source_text)} characters")
            
            print("\n8. Parsing source mappings...")
            sources = self.parse_source_mapping(source_text)
            print(f"   ✓ Extracted {len(sources)} source mappings")
        
        if len(answers_turkish) > 0:
            sample_q = list(answers_turkish.keys())[0]
            print(f"   Sample: Q{sample_q} = {answers_turkish[sample_q]['correct']}")
        
        # Combine questions with both language answers and sources
        step_num = 9 if sources else 7
        print(f"\n{step_num}. Combining questions with answers...")
        complete_questions = []
        for q in questions:
            q_id = q['id']
            if q_id in answers_turkish or q_id in answers_english:
                # Get correct answer (should be same in both)
                correct_answer = answers_turkish.get(q_id, {}).get('correct', 
                                answers_english.get(q_id, {}).get('correct', 'A'))
                
                # Get explanations from both languages
                turkish_explanation = answers_turkish.get(q_id, {}).get('explanation', 'Açıklama mevcut değil.')
                english_explanation = answers_english.get(q_id, {}).get('explanation', 'Explanation not available.')
                
                # Build question dict
                question_dict = {
                    'id': q_id,
                    'question': q['question'],
                    'options': q['options'],
                    'correct': correct_answer,
                    'explanation_turkish': turkish_explanation,
                    'explanation_english': english_explanation
                }
                
                # Add source information if available
                if q_id in sources:
                    question_dict.update({
                        'source': sources[q_id]['source'],
                        'source_chapter': sources[q_id]['source_chapter'],
                        'source_document': sources[q_id]['source_document'],
                        'source_reference': sources[q_id]['source_reference'],
                        'topic': sources[q_id]['topic']
                    })
                
                complete_questions.append(question_dict)
            else:
                # Add without answer (for debugging)
                complete_questions.append({
                    'id': q_id,
                    'question': q['question'],
                    'options': q['options'],
                    'correct': 'A',  # Default
                    'explanation_turkish': 'Cevap anahtarı PDF\'de bulunamadı.',
                    'explanation_english': 'Answer key not found in PDF.'
                })
                print(f"   ⚠ Warning: No answer found for Q{q_id}")
        
        step_num = 10 if sources else 8
        print(f"\n{step_num}. Final result: {len(complete_questions)} complete questions")
        print("=" * 80)
        
        if not complete_questions:
            print("\n❌ No questions extracted, using fallback")
            return self.get_fallback_questions()
        
        # Save a sample to file for debugging
        if len(complete_questions) > 0:
            try:
                with open('extracted_sample.txt', 'w', encoding='utf-8') as f:
                    f.write("First 3 extracted questions:\n\n")
                    for q in complete_questions[:3]:
                        f.write(f"Q{q['id']}: {q['question']}\n")
                        for opt, text in q['options'].items():
                            f.write(f"  {opt}) {text}\n")
                        f.write(f"  Correct: {q['correct']}\n")
                        f.write(f"  Turkish: {q.get('explanation_turkish', 'N/A')}\n")
                        f.write(f"  English: {q.get('explanation_english', 'N/A')}\n")
                        if 'source' in q:
                            f.write(f"  Source: {q.get('source', 'N/A')}\n")
                            f.write(f"  Chapter: {q.get('source_chapter', 'N/A')}\n")
                            f.write(f"  Document: {q.get('source_document', 'N/A')}\n")
                        f.write("\n")
                print("✓ Sample saved to 'extracted_sample.txt' for verification")
            except Exception as e:
                print(f"Could not save sample: {e}")
        
        return complete_questions
    
    def get_fallback_questions(self) -> List[Dict]:
        """Fallback questions if PDF extraction fails"""
        return [
            {
                "id": 1,
                "question": "One of the most significant economic developments in recent business history relates to the ________.",
                "options": {
                    "A": "growth of blue-chip corporations",
                    "B": "development of Pacific Rim countries",
                    "C": "entrepreneurial spirit",
                    "D": "additional employment opportunities offered by government institutions"
                },
                "correct": "C",
                "explanation_turkish": "Son iş tarihi boyunca en önemli ekonomik gelişmelerden biri girişimcilik ruhuyla ilgilidir.",
                "explanation_english": "The entrepreneurial spirit has been one of the most significant economic developments in recent business history, driving innovation, job creation, and economic growth."
            },
            {
                "id": 2,
                "question": "The profile of an entrepreneur includes ________.",
                "options": {
                    "A": "a desire for responsibility and moderate risk",
                    "B": "confidence in the ability to succeed and determination",
                    "C": "a high level of energy, a desire for immediate feedback and a future orientation",
                    "D": "All the above"
                },
                "correct": "D",
                "explanation_turkish": "Bir girişimcinin profilinde sorumluluk arzusu, ılımlı risk tercihi, başarabileceğine dair güven, kararlılık, yüksek enerji seviyesi bulunur.",
                "explanation_english": "An entrepreneur's profile encompasses all these characteristics: desire for responsibility, moderate risk preference, confidence, determination, high energy levels, desire for immediate feedback, and future orientation."
            }
        ]

# ==================== QUIZ APPLICATION CLASS ====================
class EntrepreneurshipQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("ENT 101 Entrepreneurship Quiz V2")
        self.root.geometry("1100x850")
        self.root.configure(bg="#f0f4f8")
        
        # Make window resizable
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(900, 700)
        
        # Load questions from PDFs
        self.all_questions = self.load_questions_from_pdfs()
        
        # Quiz state variables
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.answered_count = 0
        self.incorrect_questions = []
        self.start_time = None
        self.answer_submitted = False
        self.selected_answer = tk.StringVar()
        self.quiz_mode = "practice"
        self.question_range = "all"
        self.explanation_language = "english"  # New: Language preference
        
        # Initialize UI
        self.setup_styles()
        self.show_start_screen()
    
    def load_questions_from_pdfs(self) -> List[Dict]:
        """Load questions from PDF files"""
        # PDF file paths
        questions_pdf = "ENT 101 - Sample Midterm Questions.pdf"
        answers_turkish_pdf = "QuestionsExplanations.pdf"
        answers_english_pdf = "QuestionsExplanationsENG.pdf"
        source_mapping_pdf = "QuestionsSourceMapping.pdf"
        
        # Check if PDFs exist
        if not os.path.exists(questions_pdf) or not os.path.exists(answers_turkish_pdf):
            messagebox.showwarning(
                "PDF Files Not Found",
                f"Could not find PDF files:\n{questions_pdf}\n{answers_turkish_pdf}\n\nUsing fallback questions."
            )
            extractor = PDFQuestionExtractor(questions_pdf, answers_turkish_pdf, answers_english_pdf, source_mapping_pdf)
            return extractor.get_fallback_questions()
        
        # Check if English PDF exists (optional)
        if not os.path.exists(answers_english_pdf):
            print(f"Warning: {answers_english_pdf} not found. English explanations will use defaults.")
        
        # Check if source mapping PDF exists (optional)
        if not os.path.exists(source_mapping_pdf):
            print(f"Info: {source_mapping_pdf} not found. Source information will not be available.")
        
        # Check if PDF library is available
        if PDF_LIBRARY is None:
            messagebox.showinfo(
                "PDF Library Required",
                "To extract questions from PDFs, please install:\n\npip install PyPDF2 pdfplumber\n\nUsing fallback questions for now."
            )
            extractor = PDFQuestionExtractor(questions_pdf, answers_turkish_pdf, answers_english_pdf, source_mapping_pdf)
            return extractor.get_fallback_questions()
        
        # Extract questions
        try:
            extractor = PDFQuestionExtractor(questions_pdf, answers_turkish_pdf, answers_english_pdf, source_mapping_pdf)
            questions = extractor.extract_all_questions()
            
            if len(questions) < 10:
                messagebox.showwarning(
                    "Limited Questions",
                    f"Only {len(questions)} questions were extracted from PDFs.\nYou may want to check the PDF format."
                )
            else:
                messagebox.showinfo(
                    "Questions Loaded",
                    f"Successfully loaded {len(questions)} questions from PDFs!"
                )
            
            return questions
        except Exception as e:
            messagebox.showerror(
                "PDF Extraction Error",
                f"Error extracting questions:\n{str(e)}\n\nUsing fallback questions."
            )
            extractor = PDFQuestionExtractor(questions_pdf, answers_turkish_pdf, answers_english_pdf, source_mapping_pdf)
            return extractor.get_fallback_questions()
            
            return questions
        except Exception as e:
            messagebox.showerror(
                "PDF Extraction Error",
                f"Error extracting questions:\n{str(e)}\n\nUsing fallback questions."
            )
            extractor = PDFQuestionExtractor(questions_pdf, answers_turkish_pdf, answers_english_pdf)
            return extractor.get_fallback_questions()
    
    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Start.TButton', font=('Arial', 14, 'bold'), padding=15)
        style.configure('Mode.TButton', font=('Arial', 12), padding=10)
        style.configure('Action.TButton', font=('Arial', 11, 'bold'), padding=8)
        style.configure('Range.TButton', font=('Arial', 10), padding=8)
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_start_screen(self):
        """Display the start screen with mode and range selection"""
        self.clear_window()
        
        # Create a canvas with scrollbar for the start screen
        canvas = tk.Canvas(self.root, bg="#f0f4f8", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f4f8")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Update canvas width when window resizes
        def _on_canvas_resize(event):
            canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
        canvas.bind("<Configure>", _on_canvas_resize)
        
        # Main container inside scrollable frame
        container = tk.Frame(scrollable_frame, bg="#f0f4f8")
        container.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Title
        title = tk.Label(
            container,
            text="ENT 101 Entrepreneurship Quiz",
            font=('Arial', 28, 'bold'),
            bg="#f0f4f8",
            fg="#1e3a8a"
        )
        title.pack(pady=(0, 5))
        
        # Version badge
        version = tk.Label(
            container,
            text="V2.0 - PDF Auto-Extract + Range Selection",
            font=('Arial', 10, 'italic'),
            bg="#f0f4f8",
            fg="#64748b"
        )
        version.pack(pady=(0, 20))
        
        # Info box
        info_frame = tk.Frame(container, bg="white", relief='solid', borderwidth=1)
        info_frame.pack(fill='x', pady=15)
        
        info_text = f"""
        📚 Total Questions Available: {len(self.all_questions)}
        ✓ Auto-extracted from PDFs
        💡 Detailed Explanations
        📊 Flexible Study Ranges
        
        Select study mode and question range:
        """
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 11),
            bg="white",
            fg="#334155",
            justify='left',
            padx=20,
            pady=15
        )
        info_label.pack()
        
        # Question Range Selection
        range_frame = tk.LabelFrame(
            container,
            text="📊 Question Range Selection",
            font=('Arial', 12, 'bold'),
            bg="#f0f4f8",
            fg="#1e3a8a",
            padx=15,
            pady=15
        )
        range_frame.pack(fill='x', pady=15)
        
        # Range buttons
        range_buttons_frame = tk.Frame(range_frame, bg="#f0f4f8")
        range_buttons_frame.pack()
        
        self.range_var = tk.StringVar(value="all")
        
        ranges = [
            ("All Questions", "all", f"Study all {len(self.all_questions)} questions"),
            ("Random 30", "random_30", "Random 30 questions"),
            ("Random 50", "random_50", "Random 50 questions"),
            ("First 20", "first_20", "First 20 questions"),
            ("First 50", "first_50", "First 50 questions"),
            ("Custom Range", "custom", "Specify your own range")
        ]
        
        for i, (label, value, desc) in enumerate(ranges):
            rb = tk.Radiobutton(
                range_buttons_frame,
                text=f"{label}\n({desc})",
                variable=self.range_var,
                value=value,
                font=('Arial', 10),
                bg="#f0f4f8",
                fg="#334155",
                selectcolor="#bfdbfe",
                activebackground="#e0f2fe",
                padx=10,
                pady=8
            )
            rb.grid(row=i//3, column=i%3, padx=8, pady=5, sticky='w')
        
        # Custom range entry (initially hidden)
        self.custom_range_frame = tk.Frame(range_frame, bg="#f0f4f8")
        self.custom_range_frame.pack(pady=10)
        
        tk.Label(
            self.custom_range_frame,
            text="Custom Range:",
            font=('Arial', 10),
            bg="#f0f4f8"
        ).grid(row=0, column=0, padx=5)
        
        tk.Label(
            self.custom_range_frame,
            text="From:",
            font=('Arial', 10),
            bg="#f0f4f8"
        ).grid(row=0, column=1, padx=5)
        
        self.custom_start = tk.Entry(self.custom_range_frame, width=8, font=('Arial', 10))
        self.custom_start.grid(row=0, column=2, padx=5)
        self.custom_start.insert(0, "1")
        
        tk.Label(
            self.custom_range_frame,
            text="To:",
            font=('Arial', 10),
            bg="#f0f4f8"
        ).grid(row=0, column=3, padx=5)
        
        self.custom_end = tk.Entry(self.custom_range_frame, width=8, font=('Arial', 10))
        self.custom_end.grid(row=0, column=4, padx=5)
        self.custom_end.insert(0, str(len(self.all_questions)))
        
        # Language Selection for Explanations
        language_frame = tk.LabelFrame(
            container,
            text="🌍 Explanation Language / Açıklama Dili",
            font=('Arial', 12, 'bold'),
            bg="#f0f4f8",
            fg="#1e3a8a",
            padx=15,
            pady=15
        )
        language_frame.pack(fill='x', pady=15)
        
        language_desc = tk.Label(
            language_frame,
            text="Choose which language to display explanations in:",
            font=('Arial', 10),
            bg="#f0f4f8",
            fg="#64748b"
        )
        language_desc.pack(pady=(0, 10))
        
        language_buttons_frame = tk.Frame(language_frame, bg="#f0f4f8")
        language_buttons_frame.pack()
        
        self.language_var = tk.StringVar(value="english")
        
        # English option
        english_rb = tk.Radiobutton(
            language_buttons_frame,
            text="🇬🇧 English\n(English explanations)",
            variable=self.language_var,
            value="english",
            font=('Arial', 11, 'bold'),
            bg="#f0f4f8",
            fg="#334155",
            selectcolor="#bfdbfe",
            activebackground="#e0f2fe",
            padx=20,
            pady=12,
            indicatoron=True
        )
        english_rb.grid(row=0, column=0, padx=15)
        
        # Turkish option
        turkish_rb = tk.Radiobutton(
            language_buttons_frame,
            text="🇹🇷 Türkçe\n(Turkish explanations)",
            variable=self.language_var,
            value="turkish",
            font=('Arial', 11, 'bold'),
            bg="#f0f4f8",
            fg="#334155",
            selectcolor="#bfdbfe",
            activebackground="#e0f2fe",
            padx=20,
            pady=12,
            indicatoron=True
        )
        turkish_rb.grid(row=0, column=1, padx=15)
        
        # Both option
        both_rb = tk.Radiobutton(
            language_buttons_frame,
            text="🌍 Both / İkisi de\n(Show both languages)",
            variable=self.language_var,
            value="both",
            font=('Arial', 11, 'bold'),
            bg="#f0f4f8",
            fg="#334155",
            selectcolor="#bfdbfe",
            activebackground="#e0f2fe",
            padx=20,
            pady=12,
            indicatoron=True
        )
        both_rb.grid(row=0, column=2, padx=15)
        
        # Mode selection
        modes_label = tk.Label(
            container,
            text="🎯 Study Mode Selection",
            font=('Arial', 12, 'bold'),
            bg="#f0f4f8",
            fg="#1e3a8a"
        )
        modes_label.pack(pady=(15, 10))
        
        modes_frame = tk.Frame(container, bg="#f0f4f8")
        modes_frame.pack(pady=10)
        
        # Practice Mode
        practice_btn = ttk.Button(
            modes_frame,
            text="🎯 Practice Mode\n(See answers immediately)",
            style='Mode.TButton',
            command=lambda: self.start_quiz("practice")
        )
        practice_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # Test Mode
        test_btn = ttk.Button(
            modes_frame,
            text="📝 Test Mode\n(Complete before results)",
            style='Mode.TButton',
            command=lambda: self.start_quiz("test")
        )
        test_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Review Mode
        review_btn = ttk.Button(
            modes_frame,
            text="🔍 Review Mode\n(Revisit missed questions)",
            style='Mode.TButton',
            command=lambda: self.start_quiz("review")
        )
        review_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Keyboard shortcuts info
        shortcuts = tk.Label(
            container,
            text="⌨ Shortcuts: Enter = Submit | Arrow Keys = Navigate | Esc = Menu",
            font=('Arial', 9, 'italic'),
            bg="#f0f4f8",
            fg="#64748b"
        )
        shortcuts.pack(side='bottom', pady=10)
    
    def get_questions_by_range(self, range_type: str) -> List[Dict]:
        """Get questions based on selected range"""
        all_q = self.all_questions.copy()
        
        if range_type == "all":
            return all_q
        
        elif range_type == "random_30":
            return random.sample(all_q, min(30, len(all_q)))
        
        elif range_type == "random_50":
            return random.sample(all_q, min(50, len(all_q)))
        
        elif range_type == "first_20":
            return all_q[:20]
        
        elif range_type == "first_50":
            return all_q[:50]
        
        elif range_type == "custom":
            try:
                start = int(self.custom_start.get())
                end = int(self.custom_end.get())
                
                if start < 1 or end > len(all_q) or start > end:
                    messagebox.showerror(
                        "Invalid Range",
                        f"Please enter valid range (1 to {len(all_q)})"
                    )
                    return all_q
                
                # Filter questions by ID range
                return [q for q in all_q if start <= q['id'] <= end]
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for custom range")
                return all_q
        
        return all_q
    
    def start_quiz(self, mode: str):
        """Initialize and start the quiz"""
        self.quiz_mode = mode
        
        # Capture language selection
        self.explanation_language = self.language_var.get()
        
        # Get questions based on selected range
        range_type = self.range_var.get()
        
        if mode == "review" and self.incorrect_questions:
            self.questions = self.incorrect_questions.copy()
            messagebox.showinfo(
                "Review Mode",
                f"Reviewing {len(self.questions)} incorrectly answered questions."
            )
        elif mode == "review":
            messagebox.showinfo(
                "Review Mode",
                "No incorrect questions to review yet. Start with Practice or Test mode first!"
            )
            return
        else:
            self.questions = self.get_questions_by_range(range_type)
            random.shuffle(self.questions)
        
        if not self.questions:
            messagebox.showerror("Error", "No questions available!")
            return
        
        # Reset state
        self.current_question_index = 0
        self.score = 0
        self.answered_count = 0
        self.start_time = datetime.now()
        
        # Show first question
        self.show_question()
    
    def show_question(self):
        """Display the current question"""
        self.clear_window()
        self.answer_submitted = False
        self.selected_answer.set("")
        
        question = self.questions[self.current_question_index]
        
        # Create a canvas with scrollbar for the question screen
        canvas = tk.Canvas(self.root, bg="#f0f4f8", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f4f8")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Main container inside scrollable frame
        main_frame = tk.Frame(scrollable_frame, bg="#f0f4f8")
        main_frame.pack(expand=True, fill='both', padx=30, pady=20)
        
        # Store reference for dynamic wraplength updates
        self.current_main_frame = main_frame
        
        # Header with progress
        header_frame = tk.Frame(main_frame, bg="white", relief='solid', borderwidth=1)
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Progress indicator
        progress_text = f"Question {self.current_question_index + 1}/{len(self.questions)}"
        if self.quiz_mode != "test":
            progress_text += f" | Score: {self.score}/{self.answered_count}"
            if self.answered_count > 0:
                percentage = (self.score / self.answered_count) * 100
                progress_text += f" ({percentage:.1f}%)"
        
        progress_label = tk.Label(
            header_frame,
            text=progress_text,
            font=('Arial', 12, 'bold'),
            bg="white",
            fg="#1e3a8a",
            pady=10
        )
        progress_label.pack()
        
        # Question text - with dynamic wraplength
        question_frame = tk.Frame(main_frame, bg="white", relief='solid', borderwidth=1)
        question_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        self.question_label = tk.Label(
            question_frame,
            text=f"{question['id']}. {question['question']}",
            font=('Arial', 14, 'bold'),
            bg="white",
            fg="#1e293b",
            wraplength=self.root.winfo_width() - 120,  # Dynamic width
            justify='left',
            padx=20,
            pady=20
        )
        self.question_label.pack(anchor='w', fill='both', expand=True)
        
        # Source information (if available)
        if 'source_chapter' in question and self.quiz_mode == "practice":
            source_info_frame = tk.Frame(question_frame, bg="#e0f2fe", relief='flat')
            source_info_frame.pack(fill='x', padx=20, pady=(0, 10))
            
            source_text = f"📚 {question.get('source_chapter', '')}"
            if question.get('source_reference'):
                source_text += f" {question['source_reference']}"
            
            source_label = tk.Label(
                source_info_frame,
                text=source_text,
                font=('Arial', 9, 'italic'),
                bg="#e0f2fe",
                fg="#0369a1",
                padx=10,
                pady=5
            )
            source_label.pack(anchor='w')
        
        # Answer options
        options_frame = tk.Frame(main_frame, bg="#f0f4f8")
        options_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        self.option_buttons = {}
        self.option_radios = []  # Store for dynamic updates
        
        for key, value in question['options'].items():
            option_frame = tk.Frame(options_frame, bg="white", relief='solid', borderwidth=1)
            option_frame.pack(fill='x', pady=5)
            
            radio = tk.Radiobutton(
                option_frame,
                text=f"{key}) {value}",
                variable=self.selected_answer,
                value=key,
                font=('Arial', 12),
                bg="white",
                fg="#334155",
                activebackground="#e0f2fe",
                selectcolor="#bfdbfe",
                wraplength=self.root.winfo_width() - 140,  # Dynamic width
                justify='left',
                padx=15,
                pady=12,
                cursor="hand2"
            )
            radio.pack(anchor='w', fill='x')
            self.option_buttons[key] = (option_frame, radio)
            self.option_radios.append((radio, f"{key}) {value}"))
        
        # Bind window resize event
        self.root.bind('<Configure>', self._on_window_resize)
        
        # Explanation frame (hidden initially)
        self.explanation_frame = tk.Frame(main_frame, bg="#fef3c7", relief='solid', borderwidth=2)
        self.explanation_text = scrolledtext.ScrolledText(
            self.explanation_frame,
            font=('Arial', 11),
            bg="#fef3c7",
            fg="#78350f",
            wrap='word',
            height=10,
            padx=15,
            pady=15,
            relief='flat'
        )
        self.explanation_text.pack(fill='both', expand=True)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#f0f4f8")
        button_frame.pack(fill='x')
        
        # Submit button
        self.submit_btn = ttk.Button(
            button_frame,
            text="Submit Answer",
            style='Action.TButton',
            command=self.submit_answer
        )
        self.submit_btn.pack(side='left', padx=5)
        
        # Next button
        self.next_btn = ttk.Button(
            button_frame,
            text="Next Question →",
            style='Action.TButton',
            command=self.next_question,
            state='disabled'
        )
        self.next_btn.pack(side='left', padx=5)
        
        # Language toggle button (for practice/review mode)
        if self.quiz_mode in ["practice", "review"]:
            self.lang_toggle_btn = ttk.Button(
                button_frame,
                text="🌍 Switch Language",
                command=self.toggle_explanation_language
            )
            self.lang_toggle_btn.pack(side='left', padx=15)
        
        # Back to menu button
        menu_btn = ttk.Button(
            button_frame,
            text="⌂ Back to Menu",
            command=self.confirm_exit
        )
        menu_btn.pack(side='right', padx=5)
        
        # Keyboard bindings
        self.root.bind('<Return>', lambda e: self.submit_answer() if not self.answer_submitted else self.next_question())
        self.root.bind('<Right>', lambda e: self.next_question() if self.answer_submitted else None)
        self.root.bind('<Escape>', lambda e: self.confirm_exit())
    
    def submit_answer(self):
        """Process the submitted answer"""
        if self.answer_submitted:
            return
        
        selected = self.selected_answer.get()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an answer before submitting.")
            return
        
        question = self.questions[self.current_question_index]
        correct_answer = question['correct']
        
        self.answer_submitted = True
        self.answered_count += 1
        
        # Disable all radio buttons
        for key, (frame, radio) in self.option_buttons.items():
            radio.config(state='disabled')
        
        # Color code the answers
        for key, (frame, radio) in self.option_buttons.items():
            if key == correct_answer:
                frame.config(bg="#bbf7d0", borderwidth=3)
                radio.config(bg="#bbf7d0")
            elif key == selected and selected != correct_answer:
                frame.config(bg="#fecaca", borderwidth=3)
                radio.config(bg="#fecaca")
        
        # Update score
        if selected == correct_answer:
            self.score += 1
            result_icon = "✓"
            result_color = "#16a34a"
            result_text = "CORRECT!"
        else:
            result_icon = "✗"
            result_color = "#dc2626"
            result_text = f"INCORRECT! The correct answer is {correct_answer}"
            if question not in self.incorrect_questions:
                self.incorrect_questions.append(question)
        
        # Show explanation
        if self.quiz_mode in ["practice", "review"]:
            # Get explanation based on selected language
            explanation_text = ""
            
            if self.explanation_language == "english":
                explanation_text = question.get('explanation_english', question.get('explanation', 'No explanation available.'))
            elif self.explanation_language == "turkish":
                explanation_text = question.get('explanation_turkish', question.get('explanation', 'Açıklama mevcut değil.'))
            elif self.explanation_language == "both":
                turkish_exp = question.get('explanation_turkish', 'Türkçe açıklama mevcut değil.')
                english_exp = question.get('explanation_english', 'No English explanation available.')
                explanation_text = f"🇹🇷 Turkish:\n{turkish_exp}\n\n🇬🇧 English:\n{english_exp}"
            
            # Add source information if available
            source_info = ""
            if 'source_chapter' in question:
                source_info = f"\n\n📚 Source Information:"
                source_info += f"\n• Chapter: {question.get('source_chapter', 'N/A')}"
                if question.get('topic'):
                    source_info += f"\n• Topic: {question.get('topic', 'N/A')}"
                if question.get('source'):
                    source_info += f"\n• Details: {question.get('source', 'N/A')}"
                if question.get('source_reference'):
                    source_info += f"\n• Reference: {question.get('source_reference', 'N/A')}"
            
            explanation_content = f"{result_icon} {result_text}\n\n💡 Explanation:\n{explanation_text}{source_info}"
            self.explanation_text.delete('1.0', 'end')
            self.explanation_text.insert('1.0', explanation_content)
            
            self.explanation_text.tag_add("result", "1.0", "1.end")
            self.explanation_text.tag_config("result", font=('Arial', 12, 'bold'), foreground=result_color)
            
            self.explanation_frame.config(bg="#fef3c7" if selected == correct_answer else "#fee2e2")
            self.explanation_text.config(bg="#fef3c7" if selected == correct_answer else "#fee2e2")
            self.explanation_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Update buttons
        self.submit_btn.config(state='disabled')
        self.next_btn.config(state='normal')
        
        # Auto-advance in test mode
        if self.quiz_mode == "test":
            self.root.after(1000, self.next_question)
    
    def next_question(self):
        """Move to the next question or show results"""
        if not self.answer_submitted:
            return
        
        self.current_question_index += 1
        
        if self.current_question_index < len(self.questions):
            self.show_question()
        else:
            self.show_results()
    
    def _on_window_resize(self, event):
        """Handle window resize to adjust text wrapping"""
        # Only process resize events from the root window
        if event.widget != self.root:
            return
        
        # Update wraplength for question and options dynamically
        new_width = self.root.winfo_width()
        
        if hasattr(self, 'question_label') and self.question_label.winfo_exists():
            self.question_label.config(wraplength=new_width - 120)
        
        if hasattr(self, 'option_radios'):
            for radio, text in self.option_radios:
                if radio.winfo_exists():
                    radio.config(wraplength=new_width - 140)
    
    def toggle_explanation_language(self):
        """Toggle between explanation languages"""
        if self.explanation_language == "english":
            self.explanation_language = "turkish"
            new_lang = "Turkish 🇹🇷"
        elif self.explanation_language == "turkish":
            self.explanation_language = "both"
            new_lang = "Both Languages 🌍"
        else:  # both
            self.explanation_language = "english"
            new_lang = "English 🇬🇧"
        
        # Update the language variable if it exists
        if hasattr(self, 'language_var'):
            self.language_var.set(self.explanation_language)
        
        # Show message
        messagebox.showinfo("Language Changed", f"Explanation language changed to: {new_lang}")
        
        # If an answer is already submitted, refresh the explanation
        if self.answer_submitted and self.quiz_mode in ["practice", "review"]:
            question = self.questions[self.current_question_index]
            selected = self.selected_answer.get()
            correct_answer = question['correct']
            
            # Determine result
            if selected == correct_answer:
                result_icon = "✓"
                result_color = "#16a34a"
                result_text = "CORRECT!"
            else:
                result_icon = "✗"
                result_color = "#dc2626"
                result_text = f"INCORRECT! The correct answer is {correct_answer}"
            
            # Get explanation in the new language
            explanation_text = ""
            if self.explanation_language == "english":
                explanation_text = question.get('explanation_english', question.get('explanation', 'No explanation available.'))
            elif self.explanation_language == "turkish":
                explanation_text = question.get('explanation_turkish', question.get('explanation', 'Açıklama mevcut değil.'))
            elif self.explanation_language == "both":
                turkish_exp = question.get('explanation_turkish', 'Türkçe açıklama mevcut değil.')
                english_exp = question.get('explanation_english', 'No English explanation available.')
                explanation_text = f"🇹🇷 Turkish:\n{turkish_exp}\n\n🇬🇧 English:\n{english_exp}"
            
            # Add source information if available
            source_info = ""
            if 'source_chapter' in question:
                source_info = f"\n\n📚 Source Information:"
                source_info += f"\n• Chapter: {question.get('source_chapter', 'N/A')}"
                if question.get('topic'):
                    source_info += f"\n• Topic: {question.get('topic', 'N/A')}"
                if question.get('source'):
                    source_info += f"\n• Details: {question.get('source', 'N/A')}"
                if question.get('source_reference'):
                    source_info += f"\n• Reference: {question.get('source_reference', 'N/A')}"
            
            # Update explanation display
            explanation_content = f"{result_icon} {result_text}\n\n💡 Explanation:\n{explanation_text}{source_info}"
            self.explanation_text.delete('1.0', 'end')
            self.explanation_text.insert('1.0', explanation_content)
            self.explanation_text.tag_add("result", "1.0", "1.end")
            self.explanation_text.tag_config("result", font=('Arial', 12, 'bold'), foreground=result_color)
    
    def show_results(self):
        """Display the final results screen"""
        self.clear_window()
        
        # Calculate statistics
        total_questions = len(self.questions)
        correct = self.score
        incorrect = total_questions - correct
        percentage = (correct / total_questions) * 100 if total_questions > 0 else 0
        
        # Calculate time taken
        if self.start_time:
            time_taken = datetime.now() - self.start_time
            minutes = int(time_taken.total_seconds() // 60)
            seconds = int(time_taken.total_seconds() % 60)
            time_str = f"{minutes}m {seconds}s"
        else:
            time_str = "N/A"
        
        # Create a canvas with scrollbar for the results screen
        canvas = tk.Canvas(self.root, bg="#f0f4f8", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f4f8")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Main container inside scrollable frame
        container = tk.Frame(scrollable_frame, bg="#f0f4f8")
        container.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Title
        title = tk.Label(
            container,
            text="Quiz Complete! 🎉",
            font=('Arial', 28, 'bold'),
            bg="#f0f4f8",
            fg="#1e3a8a"
        )
        title.pack(pady=(0, 30))
        
        # Results box
        results_frame = tk.Frame(container, bg="white", relief='solid', borderwidth=2)
        results_frame.pack(fill='both', expand=True, pady=20)
        
        # Score display
        score_text = f"{correct}/{total_questions}"
        score_label = tk.Label(
            results_frame,
            text=score_text,
            font=('Arial', 48, 'bold'),
            bg="white",
            fg="#1e3a8a"
        )
        score_label.pack(pady=(20, 10))
        
        # Percentage
        percentage_label = tk.Label(
            results_frame,
            text=f"{percentage:.1f}%",
            font=('Arial', 32, 'bold'),
            bg="white",
            fg="#16a34a" if percentage >= 70 else "#dc2626"
        )
        percentage_label.pack(pady=(0, 20))
        
        # Performance message
        if percentage >= 90:
            message = "Outstanding! 🌟"
            color = "#16a34a"
        elif percentage >= 80:
            message = "Excellent work! 👏"
            color = "#16a34a"
        elif percentage >= 70:
            message = "Good job! 👍"
            color = "#2563eb"
        elif percentage >= 60:
            message = "Keep practicing! 📚"
            color = "#ea580c"
        else:
            message = "More study needed 💪"
            color = "#dc2626"
        
        message_label = tk.Label(
            results_frame,
            text=message,
            font=('Arial', 18, 'bold'),
            bg="white",
            fg=color
        )
        message_label.pack(pady=(0, 20))
        
        # Detailed statistics
        stats_text = f"""
        ✓ Correct Answers: {correct}
        ✗ Incorrect Answers: {incorrect}
        ⏱ Time Taken: {time_str}
        📊 Mode: {self.quiz_mode.title()}
        """
        
        stats_label = tk.Label(
            results_frame,
            text=stats_text,
            font=('Arial', 12),
            bg="white",
            fg="#334155",
            justify='left'
        )
        stats_label.pack(pady=(0, 20))
        
        # Action buttons
        button_frame = tk.Frame(container, bg="#f0f4f8")
        button_frame.pack(pady=20)
        
        # Retry button
        retry_btn = ttk.Button(
            button_frame,
            text="🔄 Try Again",
            style='Mode.TButton',
            command=lambda: self.start_quiz(self.quiz_mode)
        )
        retry_btn.grid(row=0, column=0, padx=10)
        
        # Review incorrect button
        if incorrect > 0:
            review_btn = ttk.Button(
                button_frame,
                text=f"🔍 Review {incorrect} Missed Question{'s' if incorrect != 1 else ''}",
                style='Mode.TButton',
                command=lambda: self.start_quiz("review")
            )
            review_btn.grid(row=0, column=1, padx=10)
        
        # Back to menu button
        menu_btn = ttk.Button(
            button_frame,
            text="⌂ Back to Menu",
            style='Mode.TButton',
            command=self.show_start_screen
        )
        menu_btn.grid(row=0, column=2, padx=10)
    
    def confirm_exit(self):
        """Confirm before exiting to menu"""
        if self.current_question_index > 0 and self.current_question_index < len(self.questions):
            if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit? Your progress will be lost."):
                self.show_start_screen()
        else:
            self.show_start_screen()


# ==================== MAIN EXECUTION ====================
def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = EntrepreneurshipQuiz(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
