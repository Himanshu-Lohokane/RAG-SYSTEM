# DataTrack KMRL - Helper Utilities
# Utilities for document processing

import uuid
import re
import os
import time
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

def generate_processing_id() -> str:
    """Generate a unique processing ID for document tracking"""
    return str(uuid.uuid4())

def get_file_extension(filename: str) -> str:
    """Get the file extension from a filename"""
    return os.path.splitext(filename)[1].lower()

def get_mime_type(file_extension: str) -> str:
    """Get the MIME type from a file extension"""
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.txt': 'text/plain'
    }
    return mime_types.get(file_extension.lower(), 'application/octet-stream')

def is_image_file(file_extension: str) -> bool:
    """Check if a file is an image based on extension"""
    return file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

def is_document_file(file_extension: str) -> bool:
    """Check if a file is a document based on extension"""
    return file_extension.lower() in ['.pdf', '.doc', '.docx', '.txt', '.rtf']

def format_processing_time(seconds: float) -> str:
    """Format processing time in a human-readable format"""
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} seconds"
    else:
        minutes = int(seconds / 60)
        remaining_seconds = seconds % 60
        return f"{minutes} min {remaining_seconds:.0f} sec"

def extract_form_fields_from_text(text: str) -> Dict[str, str]:
    """
    Extract form fields from text using regex patterns
    Useful for simple form extraction without computer vision
    """
    fields = {}
    
    # Common form field patterns
    patterns = {
        'name': r'(?i)name\s*[:]\s*([\w\s]+)',
        'email': r'(?i)email\s*[:]\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        'phone': r'(?i)phone\s*[:]\s*([\d\s\+\-\(\)]{8,})',
        'address': r'(?i)address\s*[:]\s*([\w\s,.#\-]+)',
        'date': r'(?i)date\s*[:]\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
        'id': r'(?i)id\s*[:]\s*([\w\d\-]+)'
    }
    
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            fields[field] = match.group(1).strip()
    
    return fields

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length and add ellipsis"""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def is_malayalam_text(text: str, threshold: float = 0.3) -> bool:
    """Check if text contains Malayalam characters above threshold"""
    if not text:
        return False
    
    # Count Malayalam characters (Unicode range)
    malayalam_chars = sum(1 for char in text if '\u0D00' <= char <= '\u0D7F')
    return malayalam_chars > len(text) * threshold

def detect_file_type(content_type: str, file_extension: str) -> str:
    """
    Detect file type based on content type and extension
    Returns: 'image', 'pdf', 'word', 'text', or 'unknown'
    """
    if content_type.startswith('image/') or is_image_file(file_extension):
        return 'image'
    elif content_type == 'application/pdf' or file_extension == '.pdf':
        return 'pdf'
    elif (content_type == 'application/msword' or 
          content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or
          file_extension in ['.doc', '.docx']):
        return 'word'
    elif content_type.startswith('text/') or file_extension == '.txt':
        return 'text'
    else:
        return 'unknown'

def sanitize_filename(filename: str) -> str:
    """Sanitize a filename to remove invalid characters"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Ensure it's not too long
    if len(filename) > 255:
        base, ext = os.path.splitext(filename)
        filename = base[:255-len(ext)] + ext
    return filename

def estimate_page_count(text_length: int) -> int:
    """Estimate page count based on text length"""
    # Rough estimate: ~500 words per page, ~6 chars per word
    chars_per_page = 3000
    return max(1, int(text_length / chars_per_page))

def format_bytes(size: int) -> str:
    """Format file size in bytes to a human-readable format"""
    power = 2 ** 10  # 1024
    n = 0
    labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {labels[n]}"
