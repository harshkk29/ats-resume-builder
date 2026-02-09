"""
Resume Parser Module
Extracts text from PDF and DOCX files
"""

import PyPDF2
from docx import Document
from typing import Optional
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeParser:
    """Parse resume files (PDF, DOCX) and extract text content"""
    
    @staticmethod
    def parse_pdf(file_path: str) -> Optional[str]:
        """
        Extract text from PDF file with enhanced error handling
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text or None if error
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"PDF file not found: {file_path}")
                return None
            
            if os.path.getsize(file_path) == 0:
                logger.error(f"PDF file is empty: {file_path}")
                return None
            
            text = ""
            with open(file_path, 'rb') as file:
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    
                    # Check if PDF is encrypted
                    if pdf_reader.is_encrypted:
                        logger.warning("PDF is encrypted, attempting to read...")
                        pdf_reader.decrypt('')
                    
                    # Extract text from all pages
                    if len(pdf_reader.pages) == 0:
                        logger.warning("PDF has no pages")
                        return None
                    
                    for page_num, page in enumerate(pdf_reader.pages):
                        try:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        except Exception as e:
                            logger.warning(f"Error extracting text from page {page_num}: {e}")
                            continue
                    
                    if not text.strip():
                        logger.warning("No text extracted from PDF")
                        return None
                    
                    logger.info(f"Successfully extracted {len(text)} characters from PDF")
                    return text.strip()
                
                except Exception as e:
                    logger.error(f"PyPDF2 error: {e}")
                    # Fallback: try alternative parsing
                    return ResumeParser._fallback_pdf_parse(file_path)
        
        except Exception as e:
            logger.error(f"Error parsing PDF: {type(e).__name__}: {e}")
            return None
    
    @staticmethod
    def _fallback_pdf_parse(file_path: str) -> Optional[str]:
        """Fallback PDF parsing method"""
        try:
            logger.info("Attempting fallback PDF parsing...")
            import pdfplumber
            
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip() if text.strip() else None
        except:
            logger.warning("Fallback PDF parsing failed")
            return None
    
    @staticmethod
    def parse_docx(file_path: str) -> Optional[str]:
        """
        Extract text from DOCX file with enhanced error handling
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text or None if error
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"DOCX file not found: {file_path}")
                return None
            
            if os.path.getsize(file_path) == 0:
                logger.error(f"DOCX file is empty: {file_path}")
                return None
            
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            if not text.strip():
                logger.warning("No text extracted from DOCX")
                return None
            
            logger.info(f"Successfully extracted {len(text)} characters from DOCX")
            return text.strip()
        except Exception as e:
            logger.error(f"Error parsing DOCX: {type(e).__name__}: {e}")
            return None
    
    @staticmethod
    def parse_resume(file_path: str) -> Optional[str]:
        """
        Parse resume file based on extension
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Extracted text or None if error
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
        
        file_extension = os.path.splitext(file_path)[1].lower()
        logger.info(f"Parsing file with extension: {file_extension}")
        
        if file_extension == '.pdf':
            return ResumeParser.parse_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            return ResumeParser.parse_docx(file_path)
        else:
            logger.error(f"Unsupported file format: {file_extension}")
            return None

