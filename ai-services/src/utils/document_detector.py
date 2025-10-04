"""
Document type detection utility
Identifies document types based on file extensions
"""

def detect_document_type(filename: str) -> str:
    """
    Detect document type based on file extension
    
    Args:
        filename: The name of the uploaded file with extension
        
    Returns: 
        str: "pdf", "doc", "docx", "image", or "unknown"
    """
    if not filename:
        return "unknown"
        
    lower_filename = filename.lower()
    
    if lower_filename.endswith('.pdf'):
        return "pdf"
    elif lower_filename.endswith('.doc'):
        return "doc"
    elif lower_filename.endswith('.docx'):
        return "docx"
    elif any(lower_filename.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']):
        return "image"
    else:
        return "unknown"