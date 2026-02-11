#!/usr/bin/env python3
import sys

try:
    import PyPDF2
    
    pdf_path = "archive_of_ashes_pt1/dub123047_dc3ae412x6_f3.pdf"
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        print(f"Number of pages: {len(pdf_reader.pages)}")
        print("\n" + "="*50)
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            print(f"\n--- Page {page_num + 1} ---")
            print(text)
            
except ImportError:
    print("PyPDF2 not installed. Trying pdfplumber...")
    try:
        import pdfplumber
        
        pdf_path = "archive_of_ashes_pt1/dub123047_dc3ae412x6_f3.pdf"
        
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Number of pages: {len(pdf.pages)}")
            print("\n" + "="*50)
            
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                print(f"\n--- Page {page_num + 1} ---")
                print(text)
                
    except ImportError:
        print("Neither PyPDF2 nor pdfplumber is installed")
        print("Please install one: pip install PyPDF2 or pip install pdfplumber")
