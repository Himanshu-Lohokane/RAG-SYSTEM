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

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from services.ocr_service import VisionService
from services.translation_service import TranslationService
from services.classification_service import ClassificationService
from models.ocr_models import KMRLDocumentProcessingResult, OCRResult, LanguageDetectionResult

# Import routers
from routers import classify, chat, document, extract, ocr

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
app.include_router(chat.router)
app.include_router(document.router)
app.include_router(extract.router)
app.include_router(ocr.router)

# CORS middleware for frontend integration - Allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins temporarily to debug
    allow_credentials=False,  # Set to False when allowing all origins
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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

# CORS preflight handler
@app.options("/{full_path:path}")
async def options_handler(request: Request):
    """Handle CORS preflight requests"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Health check endpoints
@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "DocuMind AI - Multimedia Document Processing API",
        "version": "1.0.0",
        "status": "operational",
        "description": "AI-powered document, image, video, and audio anax system",
        "endpoints": {
            "health": "/health",
            "ocr_only": "/api/ocr/extract-text",
            "language_detection": "/api/language/detect",
            "translation": "/api/translation/translate",
            "full_processing": "/api/documents/process",
            "classification": "/api/classification/document",
            "supported_languages": "/api/languages",
            "chat_advanced": "/api/chat/simple",
            "chat_simple": "/api/chat/message"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        "status": "healthy",
        "service": "DocuMind AI",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "capabilities": {
            "video_analysis": True,
            "audio_analysis": True,
            "document_ocr": True,
            "image_processing": True,
            "chat_assistant": True
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

# Note: Document processing and classification endpoints are handled by the OCR router
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
                "/api/classification/document", "/api/chat/simple"
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
    print("🚀 DocuMind AI - Multimedia Document Processing API")
    print("=" * 60)
    print("✅ Server starting up...")
    print("✅ Google Cloud Vision API ready")
    print("✅ Google Cloud Translation API ready")
    print("✅ Gemini AI ready for video/audio analysis")
    print("✅ CORS configured for frontend integration")
    print(f"✅ Upload directory ready: {UPLOAD_DIR}")
    print("=" * 60)
    port = int(os.getenv("PORT", 8001))
    if os.getenv("RENDER"):
        base_url = "https://rag-system-1-bakw.onrender.com"
    else:
        base_url = f"http://localhost:{port}"
    
    print(f"📚 API Documentation: {base_url}/docs")
    print(f"🏥 Health Check: {base_url}/health")
    print(f"🔄 Main Processing: {base_url}/api/documents/process")
    print(f"🎬 Video/Audio Analysis: Ready")
    print("=" * 60)

if __name__ == "__main__":
    import uvicorn
    print("[SERVER] Starting DataTrack KMRL OCR API server...")
    
    # Get port from environment variable (for Render deployment) or use default
    port = int(os.getenv("PORT", 8001))
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info",
        reload=False  # Disable auto-reload for production
    )
