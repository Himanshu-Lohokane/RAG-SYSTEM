"""
Document processing router
Handles endpoints for processing different document types
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from services.document_processor import DocumentProcessor

# Create router
router = APIRouter(
    prefix="/api/document",
    tags=["document"],
    responses={404: {"description": "Not found"}}
)

# Initialize the document processor service
document_processor = DocumentProcessor()

@router.post("/process")
async def process_document(file: UploadFile = File(...)):
    """
    Process document based on file type
    
    Supports:
    - PDF: Extract text and classify
    - DOC/DOCX: Extract text and classify
    - Images: OCR, translate if needed, and classify
    
    Returns:
        Document processing results including type, text, and classification
    """
    try:
        print(f"[API] Processing document: {file.filename}")
        
        # Read file bytes
        file_content = await file.read()
        
        if not file_content:
            raise HTTPException(status_code=400, detail="Empty file")
            
        # Process document with our service
        result = await document_processor.process_document(file_content, file.filename)
        
        # Return the processing result
        return result
        
    except Exception as e:
        error_msg = f"Document processing failed: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)