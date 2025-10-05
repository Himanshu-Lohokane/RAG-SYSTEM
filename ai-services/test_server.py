#!/usr/bin/env python3
"""
Simple test server to validate video/audio file upload functionality
"""
import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mimetypes

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/documents/process")
async def process_document(file: UploadFile = File(...)):
    """Test endpoint for video/audio file validation"""
    
    # Check file extension and mime type
    file_ext = os.path.splitext(file.filename)[1].lower()
    content_type = file.content_type or mimetypes.guess_type(file.filename)[0] or ""
    
    # Validate file type - UPDATED to include video and audio
    supported_exts = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx', '.mp4', '.avi', '.mov', '.mkv', '.webm', '.mp3', '.wav', '.m4a', '.aac', '.flac']
    supported_types = [
        'image/jpeg', 'image/png', 'application/pdf',
        'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'video/mp4', 'video/avi', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska', 'video/webm',
        'audio/mpeg', 'audio/wav', 'audio/x-wav', 'audio/mp4', 'audio/aac', 'audio/flac'
    ]
    
    if file_ext not in supported_exts and content_type not in supported_types:
        raise HTTPException(
            status_code=415, 
            detail=f"Unsupported file type: {content_type or file_ext}. Supported formats: JPG, PNG, PDF, DOC, DOCX, MP4, AVI, MOV, MKV, WEBM, MP3, WAV, M4A, AAC, FLAC"
        )
    
    # Mock response for testing
    if content_type.startswith('video/'):
        return {
            "success": True,
            "data": {
                "ocr": {
                    "text": "Video Analysis: This video contains various scenes with people and objects. The content appears to be a demonstration or presentation.",
                    "confidence": 0.95,
                    "method": "video_analysis",
                    "processing_time_seconds": 3.2,
                    "character_count": 120,
                    "word_count": 20
                },
                "language_detection": {
                    "language_code": "en",
                    "language_name": "English",
                    "confidence": 0.98,
                    "is_supported": True
                },
                "translation": {
                    "original_text": "Video Analysis: This video contains various scenes with people and objects. The content appears to be a demonstration or presentation.",
                    "translated_text": "Video Summary: Comprehensive video analysis showing multiple scenes, people interactions, and presentation content with high visual clarity.",
                    "source_language": "en",
                    "target_language": "en",
                    "source_language_name": "English",
                    "target_language_name": "English",
                    "error": None
                },
                "processing_info": {
                    "processing_id": "test-video-123",
                    "upload_timestamp": "2025-10-05T10:30:00Z",
                    "processing_time_seconds": 3.2
                }
            }
        }
    elif content_type.startswith('audio/'):
        return {
            "success": True,
            "data": {
                "ocr": {
                    "text": "Audio Transcription: Hello, this is a test audio recording. The speaker is discussing various topics related to technology and innovation.",
                    "confidence": 0.92,
                    "method": "audio_analysis",
                    "processing_time_seconds": 2.1,
                    "character_count": 130,
                    "word_count": 22
                },
                "language_detection": {
                    "language_code": "en",
                    "language_name": "English",
                    "confidence": 0.95,
                    "is_supported": True
                },
                "translation": {
                    "original_text": "Audio Transcription: Hello, this is a test audio recording. The speaker is discussing various topics related to technology and innovation.",
                    "translated_text": "Audio Summary: Clear recording with single speaker discussing technology and innovation topics in a professional manner.",
                    "source_language": "en",
                    "target_language": "en",
                    "source_language_name": "English",
                    "target_language_name": "English",
                    "error": None
                },
                "processing_info": {
                    "processing_id": "test-audio-456",
                    "upload_timestamp": "2025-10-05T10:30:00Z",
                    "processing_time_seconds": 2.1
                }
            }
        }
    else:
        # Default response for documents/images
        return {
            "success": True,
            "data": {
                "ocr": {
                    "text": "Sample extracted text from document or image",
                    "confidence": 0.90,
                    "method": "document",
                    "processing_time_seconds": 1.5,
                    "character_count": 45,
                    "word_count": 8
                },
                "language_detection": {
                    "language_code": "en",
                    "language_name": "English",
                    "confidence": 0.95,
                    "is_supported": True
                },
                "processing_info": {
                    "processing_id": "test-doc-789",
                    "upload_timestamp": "2025-10-05T10:30:00Z",
                    "processing_time_seconds": 1.5
                }
            }
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)