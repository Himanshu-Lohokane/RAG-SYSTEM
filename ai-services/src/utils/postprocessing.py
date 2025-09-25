# DataTrack KMRL - Text Postprocessing
# Clean and normalize extracted text

import re
import unicodedata
from typing import Dict, List, Any, Optional, Union

def clean_extracted_text(text: str) -> str:
    """
    Clean OCR extracted text
    - Remove excessive whitespace
    - Fix common OCR errors
    - Normalize punctuation
    
    Args:
        text: Raw OCR text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Replace multiple newlines with single newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Replace multiple spaces with single space
    text = re.sub(r' {2,}', ' ', text)
    
    # Fix common OCR errors
    text = text.replace('I-', 'I')  # Fix common error with capital I
    text = text.replace('|', 'I')   # Vertical bar to I
    text = text.replace('l-', 'I')  # l-hyphen to capital I
    
    # Fix broken words (words split by newline)
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKC', text)
    
    # Remove zero-width spaces and other invisible characters
    text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)
    
    # Remove excessive trailing/leading whitespace on each line
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines]
    text = '\n'.join(cleaned_lines)
    
    return text.strip()

def extract_structured_fields(text: str) -> Dict[str, str]:
    """
    Extract structured fields from text
    - Key-value pairs like "Field: Value"
    - Common document fields (date, reference number, etc.)
    
    Args:
        text: OCR text
        
    Returns:
        Dictionary of extracted fields
    """
    fields = {}
    
    # Extract key-value pairs (Field: Value)
    kv_pattern = r'([A-Za-z\s]+?):\s*(.+?)(?=\n|$)'
    matches = re.finditer(kv_pattern, text)
    
    for match in matches:
        key = match.group(1).strip()
        value = match.group(2).strip()
        
        # Skip if key or value is too short
        if len(key) < 2 or len(value) < 1:
            continue
        
        # Skip if key is too long (likely not a key)
        if len(key) > 50:
            continue
        
        # Add to fields
        fields[key] = value
    
    # Extract date (various formats)
    date_patterns = [
        r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',  # DD/MM/YYYY or MM/DD/YYYY
        r'\b(\d{2,4}[/-]\d{1,2}[/-]\d{1,2})\b',  # YYYY/MM/DD
        r'\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})\b'  # 1 Jan 2023
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match and 'Date' not in fields:
            fields['Date'] = match.group(1)
            break
    
    # Extract reference/invoice number
    ref_patterns = [
        r'\b(?:Ref(?:erence)?|Invoice|Order)\s*(?:No|Number|#)?[:\.\s]\s*([A-Za-z0-9\-\/]+)\b',
        r'\b([A-Za-z0-9]{2,}[\-\/][A-Za-z0-9\-\/]+)\b'  # Common reference format like INV-12345
    ]
    
    for pattern in ref_patterns:
        match = re.search(pattern, text)
        if match and 'Reference' not in fields:
            fields['Reference'] = match.group(1)
            break
    
    return fields

def normalize_line_breaks(text: str) -> str:
    """Normalize line breaks for consistent paragraph structure"""
    # Replace multiple line breaks with double line break
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Ensure paragraphs have double line breaks
    paragraphs = text.split('\n\n')
    normalized_paragraphs = [p.replace('\n', ' ') for p in paragraphs if p.strip()]
    
    return '\n\n'.join(normalized_paragraphs)

def correct_common_ocr_errors(text: str) -> str:
    """Correct common OCR errors in the text"""
    corrections = {
        # Numbers and special characters
        'l': '1',  # lowercase l to 1 in numeric contexts
        'O': '0',  # capital O to 0 in numeric contexts
        
        # Common errors
        'rnm': 'mm',
        'cl': 'd',
        'rn': 'm',
        'li': 'h',
        
        # Punctuation
        ''': "'",
        ''': "'",
        '"': '"',
        '"': '"',
        '…': '...',
        '–': '-',
        '—': '-'
    }
    
    # Apply corrections only in proper contexts
    result = text
    
    # Fix lowercase l as 1 in numeric contexts
    result = re.sub(r'(?<!\w)l(?=\d)', '1', result)  # l followed by digit
    result = re.sub(r'(?<=\d)l(?!\w)', '1', result)  # l preceded by digit
    result = re.sub(r'(?<=\d)l(?=\d)', '1', result)  # l between digits
    
    # Fix capital O as 0 in numeric contexts
    result = re.sub(r'(?<!\w)O(?=\d)', '0', result)  # O followed by digit
    result = re.sub(r'(?<=\d)O(?!\w)', '0', result)  # O preceded by digit
    result = re.sub(r'(?<=\d)O(?=\d)', '0', result)  # O between digits
    
    # Simple replacements for punctuation and quotes
    for error, correction in corrections.items():
        if error in ['l', 'O']:  # Skip the ones we handled with regex
            continue
        result = result.replace(error, correction)
    
    return result

def format_extracted_text(text: str, format_type: str = 'default') -> str:
    """
    Format extracted text for different purposes
    
    Args:
        text: Cleaned OCR text
        format_type: 'default', 'paragraph', 'csv', 'json'
        
    Returns:
        Formatted text
    """
    if not text:
        return ""
    
    if format_type == 'paragraph':
        # Format as continuous paragraphs
        return normalize_line_breaks(text)
    
    elif format_type == 'csv':
        # Simple CSV formatting for structured data
        lines = text.split('\n')
        csv_lines = []
        
        for line in lines:
            # Replace multiple spaces with commas
            csv_line = re.sub(r'\s{2,}', ',', line.strip())
            csv_lines.append(csv_line)
        
        return '\n'.join(csv_lines)
    
    elif format_type == 'json':
        # Basic JSON structure with fields
        fields = extract_structured_fields(text)
        
        if not fields:
            # If no structured fields, create a text field
            fields = {"text": text}
        
        # Convert to JSON string format (not actual JSON)
        json_lines = ['{']
        for key, value in fields.items():
            json_lines.append(f'  "{key}": "{value}",')
        
        # Remove last comma
        if len(json_lines) > 1:
            json_lines[-1] = json_lines[-1].rstrip(',')
        
        json_lines.append('}')
        
        return '\n'.join(json_lines)
    
    else:  # default
        # Just clean the text
        return clean_extracted_text(text)

def extract_table_data(text: str) -> List[List[str]]:
    """
    Extract table data from text
    Uses whitespace alignment to identify table structure
    
    Args:
        text: OCR text with potential table
        
    Returns:
        List of rows, each row is a list of cells
    """
    lines = text.split('\n')
    table_data = []
    
    # Find lines with consistent spacing (potential table rows)
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue
        
        # Split by multiple spaces (potential cell delimiter)
        cells = re.split(r'\s{2,}', line.strip())
        
        # If we have multiple cells, consider it a table row
        if len(cells) > 1:
            table_data.append(cells)
    
    return table_data

def standardize_date_formats(text: str) -> str:
    """Standardize date formats to YYYY-MM-DD"""
    # Pattern for DD/MM/YYYY or MM/DD/YYYY
    pattern1 = r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})'
    
    def replace_date(match):
        day_or_month1 = int(match.group(1))
        day_or_month2 = int(match.group(2))
        year = match.group(3)
        
        # Convert 2-digit year to 4-digit year
        if len(year) == 2:
            century = '19' if int(year) > 50 else '20'
            year = century + year
        
        # Try to determine if it's DD/MM or MM/DD based on values
        if day_or_month1 > 12:  # Must be day
            return f"{year}-{day_or_month2:02d}-{day_or_month1:02d}"
        else:  # Assume MM/DD
            return f"{year}-{day_or_month1:02d}-{day_or_month2:02d}"
    
    # Replace dates
    result = re.sub(pattern1, replace_date, text)
    
    # Pattern for text dates like "1 Jan 2023"
    months = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
        'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
        'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }
    
    pattern2 = r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{2,4})'
    
    def replace_text_date(match):
        day = match.group(1)
        month = match.group(2).lower()[:3]
        year = match.group(3)
        
        # Convert 2-digit year to 4-digit year
        if len(year) == 2:
            century = '19' if int(year) > 50 else '20'
            year = century + year
        
        return f"{year}-{months[month]}-{int(day):02d}"
    
    # Replace text dates (case insensitive)
    return re.sub(pattern2, replace_text_date, result, flags=re.IGNORECASE)
