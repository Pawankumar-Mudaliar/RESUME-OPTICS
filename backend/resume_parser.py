"""
Resume Parser Module
Extracts text from PDF and DOCX files
"""

import PyPDF2
from docx import Document
import re


class ResumeParser:
    """
    This class reads resume files (PDF/DOCX) and extracts text.
    """
    
    @staticmethod
    def extract_text_from_pdf(file_path):
        """
        Extract text from a PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text as string
        """
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                # Loop through all pages and extract text
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    @staticmethod
    def extract_text_from_docx(file_path):
        """
        Extract text from a DOCX (Word) file
        
        Args:
            file_path: Path to the DOCX file
            
        Returns:
            Extracted text as string
        """
        text = ""
        try:
            doc = Document(file_path)
            # Loop through all paragraphs
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    @staticmethod
    def clean_text(text):
        """
        Clean and normalize extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\-@]', '', text)
        return text.strip()
    
    @staticmethod
    def parse_resume(file_path):
        """
        Main method to parse any resume file
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Dictionary with extracted and cleaned text
        """
        if file_path.lower().endswith('.pdf'):
            raw_text = ResumeParser.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            raw_text = ResumeParser.extract_text_from_docx(file_path)
        else:
            return {"error": "Unsupported file format. Use PDF or DOCX"}
        
        cleaned_text = ResumeParser.clean_text(raw_text)
        
        return {
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "length": len(cleaned_text)
        }
