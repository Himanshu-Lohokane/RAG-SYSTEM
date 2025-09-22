# DataTrack KMRL - OCR Vision Service
# Google Cloud Vision API for document text extraction

import asyncio
import io
import sys
import os
from typing import Union, Optional, List
from google.cloud import vision

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config
from models.ocr_models import OCRResult

class VisionService:
    """Google Cloud Vision API service for KMRL document OCR processing"""
    
    def __init__(self):
        """Initialize Vision client with KMRL-specific configuration"""
        print("[VISION] Initializing Google Cloud Vision service for DataTrack-KMRL...")
        self.client = Config.get_vision_client()
        print("[VISION] ✅ Vision service ready for document processing")
    
    def extract_text(self, image_data: Union[bytes, str], method: str = 'document') -> OCRResult:
        """
        Extract text from image using OCR - Optimized for KMRL documents
        
        Args:
            image_data: Image as bytes or file path
            method: 'document' (recommended for KMRL docs) or 'text' (basic OCR)
            
        Returns:
            OCRResult: Extracted text with confidence and metadata
        """
        print(f"[VISION] Starting OCR processing with method: {method}")
        
        try:
            # Handle different input types
            if isinstance(image_data, str):
                print(f"[VISION] Reading image from file: {image_data}")
                with open(image_data, 'rb') as image_file:
                    content = image_file.read()
            else:
                print(f"[VISION] Processing image from bytes (size: {len(image_data)} bytes)")
                content = image_data
            
            image = vision.Image(content=content)
            
            # Choose OCR method based on KMRL document requirements
            if method == 'document':
                print("[VISION] Using document text detection (recommended for KMRL reports/forms)")
                response = self.client.document_text_detection(image=image)
                
                if response.error.message:
                    error_msg = f"Vision API Error: {response.error.message}"
                    print(f"[VISION] ❌ {error_msg}")
                    return OCRResult(
                        text="",
                        confidence=0.0,
                        method=method,
                        error=error_msg
                    )
                
                if response.full_text_annotation:
                    text = response.full_text_annotation.text
                    # Calculate confidence from page confidence
                    confidence = (
                        response.full_text_annotation.pages[0].confidence 
                        if response.full_text_annotation.pages 
                        else 0.0
                    )
                    print(f"[VISION] ✅ Document OCR completed - Confidence: {confidence:.2f}")
                    print(f"[VISION] Extracted text length: {len(text)} characters")
                else:
                    text = ""
                    confidence = 0.0
                    print("[VISION] ⚠️ No text detected in document")
                    
            else:  # Basic text detection
                print("[VISION] Using basic text detection")
                response = self.client.text_detection(image=image)
                
                if response.error.message:
                    error_msg = f"Vision API Error: {response.error.message}"
                    print(f"[VISION] ❌ {error_msg}")
                    return OCRResult(
                        text="",
                        confidence=0.0,
                        method=method,
                        error=error_msg
                    )
                
                if response.text_annotations:
                    text = response.text_annotations[0].description
                    confidence = 1.0  # Text detection doesn't provide confidence
                    print(f"[VISION] ✅ Basic text extraction completed")
                    print(f"[VISION] Extracted text length: {len(text)} characters")
                else:
                    text = ""
                    confidence = 0.0
                    print("[VISION] ⚠️ No text detected in image")
            
            # Log first 100 characters for debugging (without exposing sensitive data)
            preview = text[:100] + "..." if len(text) > 100 else text
            print(f"[VISION] Text preview: {preview}")
            
            return OCRResult(
                text=text,
                confidence=confidence,
                method=method,
                error=None
            )
            
        except Exception as e:
            error_msg = f"OCR processing failed: {str(e)}"
            print(f"[VISION] ❌ {error_msg}")
            return OCRResult(
                text="",
                confidence=0.0,
                method=method,
                error=error_msg
            )
    
    def detect_document_features(self, image_data: Union[bytes, str]) -> dict:
        """
        Detect document features like tables, forms - Useful for KMRL structured documents
        
        Args:
            image_data: Image as bytes or file path
            
        Returns:
            Dictionary with detected document features
        """
        print("[VISION] Analyzing document structure and features...")
        
        try:
            if isinstance(image_data, str):
                with open(image_data, 'rb') as image_file:
                    content = image_file.read()
            else:
                content = image_data
            
            image = vision.Image(content=content)
            
            # Get document text detection with structure
            response = self.client.document_text_detection(image=image)
            
            if response.error.message:
                raise Exception(f"Vision API Error: {response.error.message}")
            
            features = {
                'has_text': bool(response.full_text_annotation),
                'page_count': len(response.full_text_annotation.pages) if response.full_text_annotation else 0,
                'blocks': [],
                'paragraphs': [],
                'words': []
            }
            
            if response.full_text_annotation:
                for page in response.full_text_annotation.pages:
                    for block in page.blocks:
                        features['blocks'].append({
                            'confidence': block.confidence,
                            'block_type': block.block_type.name if hasattr(block, 'block_type') else 'TEXT'
                        })
                        
                        for paragraph in block.paragraphs:
                            features['paragraphs'].append({
                                'confidence': paragraph.confidence
                            })
                            
                            for word in paragraph.words:
                                features['words'].append({
                                    'confidence': word.confidence,
                                    'text': ''.join([symbol.text for symbol in word.symbols])
                                })
            
            print(f"[VISION] ✅ Document analysis completed:")
            print(f"[VISION]   - Pages: {features['page_count']}")
            print(f"[VISION]   - Text blocks: {len(features['blocks'])}")
            print(f"[VISION]   - Paragraphs: {len(features['paragraphs'])}")
            print(f"[VISION]   - Words: {len(features['words'])}")
            
            return features
            
        except Exception as e:
            error_msg = f"Document feature detection failed: {str(e)}"
            print(f"[VISION] ❌ {error_msg}")
            raise Exception(error_msg)
    
    def detect_handwriting(self, image_data: Union[bytes, str]) -> OCRResult:
        """
        Detect handwritten text - Useful for KMRL handwritten forms/signatures
        
        Args:
            image_data: Image as bytes or file path
            
        Returns:
            OCRResult with handwritten text extraction
        """
        print("[VISION] Processing handwritten text detection...")
        
        try:
            if isinstance(image_data, str):
                with open(image_data, 'rb') as image_file:
                    content = image_file.read()
            else:
                content = image_data
            
            image = vision.Image(content=content)
            
            # Use document text detection which handles handwriting better
            response = self.client.document_text_detection(image=image)
            
            if response.error.message:
                return OCRResult(
                    text="",
                    confidence=0.0,
                    method="handwriting",
                    error=f"Vision API Error: {response.error.message}"
                )
            
            if response.full_text_annotation:
                text = response.full_text_annotation.text
                confidence = (
                    response.full_text_annotation.pages[0].confidence 
                    if response.full_text_annotation.pages 
                    else 0.0
                )
                print(f"[VISION] ✅ Handwriting detection completed - Confidence: {confidence:.2f}")
            else:
                text = ""
                confidence = 0.0
                print("[VISION] ⚠️ No handwritten text detected")
            
            return OCRResult(
                text=text,
                confidence=confidence,
                method="handwriting",
                error=None
            )
            
        except Exception as e:
            error_msg = f"Handwriting detection failed: {str(e)}"
            print(f"[VISION] ❌ {error_msg}")
            return OCRResult(
                text="",
                confidence=0.0,
                method="handwriting",
                error=error_msg
            )
    
    async def extract_text_async(self, image_data: Union[bytes, str], method: str = 'document') -> OCRResult:
        """Async version of extract_text for high-performance processing"""
        print("[VISION] Running async OCR processing...")
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.extract_text, image_data, method)
