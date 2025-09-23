"""
Router for document classification endpoints using Google Cloud Natural Language API
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Optional
from pydantic import BaseModel
from services.classification_service import ClassificationService

router = APIRouter(prefix="/classify", tags=["classification"])

class ClassificationRequest(BaseModel):
    """Request model for document classification"""
    text: str
    min_confidence: Optional[float] = 0.0

class ClassificationResponse(BaseModel):
    """Response model for document classification"""
    category: str
    confidence: float
    all_categories: list
    processing_time_seconds: float
    method: str

# Create a single instance of the classification service
classification_service = ClassificationService()

def get_classification_service() -> ClassificationService:
    """Dependency to get classification service instance"""
    return classification_service

@router.post("/text", response_model=ClassificationResponse)
async def classify_text(
    request: ClassificationRequest,
    service: ClassificationService = Depends(get_classification_service)
) -> Dict:
    """
    Classify document based on text content using Google Cloud Natural Language API
    
    This endpoint uses Google's pre-trained models to classify documents without
    requiring custom training data. The API automatically categorizes text content
    into categories with confidence scores.
    
    Parameters:
        request: Classification request with text content
        
    Returns:
        ClassificationResponse with category, confidence score, and all possible categories
    """
    try:
        if not request.text or len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text content is required")
        
        # Classify the document using the service
        result = service.classify_document(request.text)
        
        # Filter by minimum confidence if specified
        if request.min_confidence > 0 and result["confidence"] < request.min_confidence:
            result["category"] = "Unknown"
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")
