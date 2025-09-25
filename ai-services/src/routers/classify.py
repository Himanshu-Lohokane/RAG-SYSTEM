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
        # Validate request
        if not request:
            raise HTTPException(
                status_code=400,
                detail="Request body is required"
            )
            
        # Validate text content
        if not request.text or len(request.text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Text content is required and cannot be empty"
            )
            
        # Check if text is too long
        if len(request.text) > 100000:  # Limit text length for classification
            print(f"[API] ⚠️ Text too long for classification, truncating: {len(request.text)} chars")
            request.text = request.text[:100000]
            
        # Validate confidence threshold
        if request.min_confidence is not None and (request.min_confidence < 0 or request.min_confidence > 1):
            raise HTTPException(
                status_code=400,
                detail="Minimum confidence must be between 0.0 and 1.0"
            )
            
        print(f"[API] Document classification request - Text length: {len(request.text)} chars")
        
        try:
            # Classify the document using the service
            result = service.classify_document(request.text)
            
            # Validate the service result
            if not result:
                raise HTTPException(
                    status_code=500,
                    detail="Classification service returned empty result"
                )
                
            if "category" not in result or "confidence" not in result:
                raise HTTPException(
                    status_code=500,
                    detail="Classification service returned incomplete result"
                )
                
        except ValueError as ve:
            raise HTTPException(
                status_code=422,
                detail=f"Classification service validation error: {str(ve)}"
            )
        except NotImplementedError:
            raise HTTPException(
                status_code=501,
                detail="Classification method not implemented or unavailable"
            )
        
        # Filter by minimum confidence if specified
        if request.min_confidence > 0 and result["confidence"] < request.min_confidence:
            print(f"[API] ⚠️ Classification confidence {result['confidence']} below threshold {request.min_confidence}")
            result["category"] = "Unknown"
            
        print(f"[API] ✅ Classification completed - Category: {result['category']}, Confidence: {result['confidence']}")
        
        return result
        
    except HTTPException:
        # Pass through HTTP exceptions
        raise
        
    except ValueError as ve:
        error_msg = f"Classification validation error: {str(ve)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=400,
            detail=error_msg
        )
        
    except Exception as e:
        error_msg = f"Classification error: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )
