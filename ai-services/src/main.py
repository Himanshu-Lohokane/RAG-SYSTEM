# DataTrack KMRL - Main FastAPI Application
# OCR and Document Processing Server for KMRL Metro Rail

import time
import uuid
from datetime import datetime
from typing import Union, Dict, List, Optional, Any
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from services.ocr_service import VisionService
from services.translation_service import TranslationService
from services.classification_service import ClassificationService
from models.ocr_models import KMRLDocumentProcessingResult, OCRResult, LanguageDetectionResult

# Import routers
from routers import classify

# Initialize FastAPI app
app = FastAPI(
    title="DataTrack KMRL - OCR & Document Processing API",
    description="AI-powered document processing system for Kochi Metro Rail Limited (KMRL)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(classify.router)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory for temporary file storage
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
print(f"[SERVER] Upload directory created/verified: {UPLOAD_DIR}")

# Dependency injection for services
def get_vision_service() -> VisionService:
    """Dependency injection for OCR service"""
    return VisionService()

def get_translation_service() -> TranslationService:
    """Dependency injection for translation service"""
    return TranslationService()

def get_classification_service() -> ClassificationService:
    """Dependency injection for document classification service"""
    print("[API] Initializing Google Natural Language API classification service")
    return ClassificationService()

# Health check endpoints
@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "DataTrack KMRL - OCR & Document Processing API",
        "version": "1.0.0",
        "status": "operational",
        "description": "AI-powered document processing for Kochi Metro Rail Limited",
        "endpoints": {
            "health": "/health",
            "ocr_only": "/api/ocr/extract-text",
            "language_detection": "/api/language/detect",
            "translation": "/api/translation/translate",
            "full_processing": "/api/documents/process",
            "classification": "/api/classification/document",
            "supported_languages": "/api/languages"
        }
    }


# Utility Endpoints
@app.get("/api/languages")
async def get_supported_languages(
    translation_service: TranslationService = Depends(get_translation_service)
):
    """Get list of supported languages with KMRL primary languages highlighted"""
    try:
        languages = translation_service.get_supported_languages()
        return {
            "success": True,
            "data": {
                "languages": languages,
                "kmrl_primary": ["English", "Malayalam"],
                "total_count": len(languages)
            }
        }
    except Exception as e:
        raise HTTPException(500, f"Failed to get supported languages: {str(e)}")
    


# OCR Endpoints
@app.post("/api/ocr/extract-text")
async def extract_text_only(
    file: UploadFile = File(...),
    ocr_method: str = "document",
    vision_service: VisionService = Depends(get_vision_service)
):
    """
    Extract text from uploaded image (OCR only)
    
    - **file**: Image file (PNG, JPG, PDF supported)
    - **ocr_method**: 'document' (recommended for KMRL docs) or 'text' (basic)
    """
    print(f"[API] OCR request received - File: {file.filename}, Method: {ocr_method}")
    
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, f"Invalid file type: {file.content_type}. Only images are supported.")
        
        # Read image data
        image_data = await file.read()
        print(f"[API] Image loaded: {len(image_data)} bytes")
        
        # Process OCR
        start_time = time.time()
        ocr_result = vision_service.extract_text(image_data, method=ocr_method)
        processing_time = time.time() - start_time
        
        # Check for OCR errors
        if ocr_result.error:
            print(f"[API] ❌ OCR failed: {ocr_result.error}")
            raise HTTPException(500, f"OCR processing failed: {ocr_result.error}")
        
        print(f"[API] ✅ OCR completed successfully in {processing_time:.2f}s")
        
        return {
            "success": True,
            "data": {
                "text": ocr_result.text,
                "confidence": ocr_result.confidence,
                "method": ocr_result.method,
                "processing_time_seconds": round(processing_time, 3),
                "character_count": len(ocr_result.text),
                "word_count": len(ocr_result.text.split()) if ocr_result.text else 0
            },
            "metadata": {
                "filename": file.filename,
                "file_size": len(image_data),
                "processed_at": datetime.now().isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Unexpected error during OCR processing: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        raise HTTPException(500, error_msg)

# Language Detection Endpoint
@app.post("/api/language/detect")
async def detect_language(
    text: str,
    translation_service: TranslationService = Depends(get_translation_service)
):
    """
    Detect language of text - Optimized for KMRL English/Malayalam detection
    
    - **text**: Text to analyze for language detection
    """
    print(f"[API] Language detection request - Text length: {len(text)} chars")
    
    try:
        detection_result = translation_service.detect_language(text)
        
        if detection_result.error:
            print(f"[API] ❌ Language detection failed: {detection_result.error}")
            raise HTTPException(500, f"Language detection failed: {detection_result.error}")
        
        print(f"[API] ✅ Language detected: {detection_result.language_name}")
        
        return {
            "success": True,
            "data": {
                "language_code": detection_result.language_code,
                "language_name": detection_result.language_name,
                "confidence": detection_result.confidence,
                "is_kmrl_primary": detection_result.language_code in ['en', 'ml']
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Unexpected error during language detection: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        raise HTTPException(500, error_msg)

# Translation Endpoint
@app.post("/api/translation/translate")
async def translate_text(
    text: str,
    target_language: str = "en",
    source_language: str = None,
    translation_service: TranslationService = Depends(get_translation_service)
):
    """
    Translate text - Focused on KMRL Malayalam ↔ English translation
    
    - **text**: Text to translate
    - **target_language**: Target language code (default: 'en')
    - **source_language**: Source language (auto-detect if not provided)
    """
    print(f"[API] Translation request - Target: {target_language}, Text length: {len(text)} chars")
    
    try:
        translation_result = translation_service.translate_text(
            text, target_language, source_language
        )
        
        if translation_result.error:
            print(f"[API] ❌ Translation failed: {translation_result.error}")
            raise HTTPException(500, f"Translation failed: {translation_result.error}")
        
        print(f"[API] ✅ Translation completed: {translation_result.source_language_name} → {translation_result.target_language_name}")
        
        return {
            "success": True,
            "data": translation_result.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Unexpected error during translation: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        raise HTTPException(500, error_msg)

# Complete Document Processing Endpoint
@app.post("/api/documents/process")
async def process_document(
    file: UploadFile = File(...),
    ocr_method: str = "document",
    target_language: str = "en",
    include_translation: bool = False,
    vision_service: VisionService = Depends(get_vision_service),
    translation_service: TranslationService = Depends(get_translation_service)
):
    """
    Complete document processing workflow for KMRL documents
    
    - **file**: Document image file
    - **ocr_method**: 'document' (recommended) or 'text'
    - **target_language**: Language for translation (if enabled)
    - **include_translation**: Whether to include translation in processing
    """
    processing_id = str(uuid.uuid4())
    print(f"[API] Document processing started - ID: {processing_id}, File: {file.filename}")
    
    try:
        # Validate file
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, f"Invalid file type: {file.content_type}")
        
        # Read image data
        image_data = await file.read()
        start_time = time.time()
        
        # Step 1: OCR Processing
        print(f"[API] Step 1/3: OCR processing...")
        ocr_result = vision_service.extract_text(image_data, method=ocr_method)
        
        if ocr_result.error:
            raise HTTPException(500, f"OCR failed: {ocr_result.error}")
        
        # Step 2: Language Detection
        print(f"[API] Step 2/3: Language detection...")
        language_detection = translation_service.detect_language(ocr_result.text)
        
        if language_detection.error:
            # Non-fatal error - continue processing
            print(f"[API] ⚠️ Language detection warning: {language_detection.error}")
        
        # Step 3: Translation (if requested)
        translation_result = None
        if include_translation and ocr_result.text:
            print(f"[API] Step 3/3: Translation processing...")
            translation_result = translation_service.translate_text(
                ocr_result.text, target_language
            )
            if translation_result.error:
                print(f"[API] ⚠️ Translation warning: {translation_result.error}")
        else:
            print(f"[API] Step 3/3: Translation skipped (not requested)")
        
        processing_time = time.time() - start_time
        
        # Build complete result
        result = KMRLDocumentProcessingResult(
            filename=file.filename,
            file_size=len(image_data),
            upload_timestamp=datetime.now().isoformat(),
            processing_id=processing_id,
            ocr_result=ocr_result,
            language_detection=language_detection,
            translation_result=translation_result,
            processing_time_seconds=round(processing_time, 3),
            success=True,
            errors=[]
        )
        
        print(f"[API] ✅ Document processing completed successfully in {processing_time:.2f}s")
        
        return {
            "success": True,
            "data": result.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Document processing failed: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        raise HTTPException(500, error_msg)


# Document Classification Endpoints

# Simple text classification endpoint - perfect for Swagger UI
@app.post("/api/classification/text")
async def classify_text_api(
    text: str = Body(..., description="The text content to classify", example="This is a sample document about safety procedures for equipment operation"),
    classification_service: ClassificationService = Depends(get_classification_service)
):
    """
    Simply paste your text here to classify it
    
    Returns the document category with confidence score
    """
    try:
        # Process the document
        print(f"[API] Classifying text with length: {len(text)}")
        start_time = time.time()
        classification_result = classification_service.classify_document(text)
        total_processing_time = time.time() - start_time
        
        # Return simple result
        print(f"[API] ✅ Document classification completed - Category: {classification_result['category']}")
        return {
            "success": True,
            "data": {
                "processing_time_seconds": round(total_processing_time, 3),
                "classification": {
                    "category": classification_result["category"],
                    "confidence": classification_result["confidence"],
                    "all_categories": classification_result["all_categories"],
                    "processing_time_seconds": classification_result.get("processing_time_seconds", 0),
                    "method": classification_result.get("method", "unknown")
                },
                "text_preview": text[:200] + "..." if len(text) > 200 else text
            }
        }
    except Exception as e:
        print(f"[API] ❌ Classification error: {str(e)}")
        return {
            "success": False,
            "error": f"Classification failed: {str(e)}"
        }

# Document-based classification endpoint (with OCR)
@app.post("/api/classification/document")
async def classify_document(
    file: UploadFile = File(...),
    vision_service: VisionService = Depends(get_vision_service),
    classification_service: ClassificationService = Depends(get_classification_service)
):
    """
    Extract text using OCR and classify the document into predefined KMRL categories
    
    - **file**: The document file to classify (image)
    """
    print(f"[API] Classification request received - File: {file.filename}")
    
    try:
        # Validate file
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, f"Invalid file type: {file.content_type}. Only images are supported.")
        
        # Read file content
        image_data = await file.read()
        start_time = time.time()
        
        # Extract text using OCR
        print(f"[API] Step 1/2: Extracting text for classification...")
        ocr_result = vision_service.extract_text(image_data, method="document")
        
        if ocr_result.error:
            raise HTTPException(500, f"Text extraction failed: {ocr_result.error}")
        
        # Classify the document based on extracted text
        print(f"[API] Step 2/2: Classifying document...")
        classification_result = classification_service.classify_document(ocr_result.text)
        
        total_processing_time = time.time() - start_time
        
        # Return classification results
        print(f"[API] ✅ Document classification completed - Category: {classification_result['category']}")
        return {
            "success": True,
            "data": {
                "filename": file.filename,
                "file_size": len(image_data),
                "content_type": file.content_type,
                "processing_time_seconds": round(total_processing_time, 3),
                "classification": classification_result,
                "text_preview": ocr_result.text[:200] + "..." if len(ocr_result.text) > 200 else ocr_result.text
            }
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"[API] ❌ Classification error: {str(e)}")
        return {
            "success": False,
            "error": f"Classification failed: {str(e)}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error classifying document: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        raise HTTPException(500, error_msg)

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found",
            "message": "The requested endpoint does not exist",
            "available_endpoints": [
                "/docs", "/health", "/api/ocr/extract-text", 
                "/api/documents/process", "/api/languages", 
                "/api/classification/document"
            ]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred during processing"
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("🚀 DataTrack KMRL - OCR & Document Processing API")
    print("=" * 60)
    print("✅ Server starting up...")
    print("✅ Google Cloud Vision API ready")
    print("✅ Google Cloud Translation API ready")
    print("✅ CORS configured for frontend integration")
    print(f"✅ Upload directory ready: {UPLOAD_DIR}")
    print("=" * 60)
    print("📚 API Documentation: http://localhost:8001/docs")
    print("🏥 Health Check: http://localhost:8001/health")
    print("🔄 Main Processing: http://localhost:8001/api/documents/process")
    print("=" * 60)

if __name__ == "__main__":
    import uvicorn
    print("[SERVER] Starting DataTrack KMRL OCR API server...")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001,
        log_level="info",
        reload=True  # Enable auto-reload during development
    )
