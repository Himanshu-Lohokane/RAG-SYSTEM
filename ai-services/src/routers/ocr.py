# DataTrack KMRL - OCR Endpoints
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
import uuid
import os
import io
import time
import sys
import json
import asyncio
from PIL import Image
import pypdfium2 as pdfium
import PyPDF2  # Added for direct PDF text extraction
import docx2txt
import tempfile
import shutil
import mimetypes

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ocr_service import VisionService
from services.classification_service import ClassificationService
from services.extraction_service import EntityExtractionService
from utils.preprocessing import preprocess_image
from utils.postprocessing import clean_extracted_text
from utils.helpers import generate_processing_id

# Initialize router
router = APIRouter(prefix="/api/documents", tags=["document-processing"])

# Initialize services
vision_service = VisionService()
classification_service = ClassificationService()
extraction_service = EntityExtractionService()

# Configure temp directory for file processing
TEMP_DIR = os.path.join(tempfile.gettempdir(), "datatrack-kmrl-processing")
os.makedirs(TEMP_DIR, exist_ok=True)

# Storage for processing results (for demo/dev purposes)
# In production, this would use a database
processing_results = {}

@router.post("/process")
async def process_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    ocr_method: str = Form("document"),
    include_translation: bool = Form(False),
    target_language: str = Form("en")
):
    """
    Process uploaded document for OCR text extraction
    - Handles images (JPG, PNG), PDFs, and Word documents (DOC, DOCX)
    - Performs OCR on images or extracts text from documents
    - Optionally translates text if requested
    """
    start_time = time.time()
    processing_id = generate_processing_id()
    temp_file_path = None
    
    print(f"[API] Starting document processing (ID: {processing_id})")
    print(f"[API] File: {file.filename}, Method: {ocr_method}")
    print(f"[API] Translation requested: {include_translation}, Target: {target_language}")
    
    try:
        # Validate file exists
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
            
        # Validate file size (50MB limit)
        file_size_mb = 0
        try:
            # Get file size by reading a chunk and checking the position
            file_size = 0
            chunk = await file.read(1024 * 1024)  # Read 1MB
            while chunk:
                file_size += len(chunk)
                if file_size > 50 * 1024 * 1024:  # 50MB limit
                    raise HTTPException(status_code=413, detail="File too large. Maximum size is 50MB")
                chunk = await file.read(1024 * 1024)
            
            # Reset file position
            await file.seek(0)
            file_size_mb = file_size / (1024 * 1024)
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
        
        # Check file extension and mime type
        file_ext = os.path.splitext(file.filename)[1].lower()
        content_type = file.content_type or mimetypes.guess_type(file.filename)[0] or ""
        
        # Validate file type
        supported_exts = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']
        supported_types = [
            'image/jpeg', 'image/png', 'application/pdf',
            'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        
        if file_ext not in supported_exts and content_type not in supported_types:
            raise HTTPException(
                status_code=415, 
                detail=f"Unsupported file type: {content_type or file_ext}. Supported formats: JPG, PNG, PDF, DOC, DOCX"
            )
        
        # Create temp file path
        temp_file_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}{file_ext}")
        
        # Save uploaded file
        try:
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except IOError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save temporary file: {str(e)}"
            )
        
        # Process based on file type
        extracted_text = ""
        confidence = 0.0
        
        # Image processing (JPG, PNG, etc.)
        if content_type.startswith('image/'):
            print(f"[API] Processing image file: {file.filename}")
            
            try:
                # Verify image can be opened
                try:
                    with Image.open(temp_file_path) as img:
                        img_width, img_height = img.size
                        if img_width < 50 or img_height < 50:
                            raise HTTPException(
                                status_code=400,
                                detail="Image too small for effective OCR processing. Minimum dimensions: 50x50px"
                            )
                except IOError as e:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Invalid or corrupted image file: {str(e)}"
                    )
                
                # Preprocess image for better OCR results
                try:
                    preprocessed_image = await preprocess_image(temp_file_path)
                except Exception as e:
                    print(f"[API] ⚠️ Image preprocessing failed: {str(e)}. Using original image.")
                    with open(temp_file_path, 'rb') as f:
                        preprocessed_image = f.read()
                
                # Extract text using Vision API
                try:
                    ocr_result = await vision_service.extract_text_async(
                        preprocessed_image, 
                        method=ocr_method
                    )
                    
                    if ocr_result.error:
                        raise HTTPException(
                            status_code=422,
                            detail=f"OCR processing failed: {ocr_result.error}"
                        )
                        
                    extracted_text = ocr_result.text
                    confidence = ocr_result.confidence
                    
                except Exception as e:
                    if isinstance(e, HTTPException):
                        raise e
                    raise HTTPException(
                        status_code=500,
                        detail=f"Vision API error during OCR processing: {str(e)}"
                    )
            
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Image processing failed: {str(e)}"
                )
            
        # PDF processing
        elif content_type == 'application/pdf' or file_ext.lower() == '.pdf':
            print(f"[API] Processing PDF file: {file.filename}")
            
            try:
                # Verify PDF can be opened
                try:
                    with open(temp_file_path, 'rb') as pdf_file:
                        # Try to open with PyPDF2 first (this is faster and more accurate for text PDFs)
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        page_count = len(pdf_reader.pages)
                        
                        if page_count == 0:
                            raise HTTPException(
                                status_code=400,
                                detail="PDF file contains no pages"
                            )
                        elif page_count > 50:
                            raise HTTPException(
                                status_code=413,
                                detail=f"PDF has too many pages ({page_count}). Maximum allowed: 50 pages"
                            )
                except Exception as e:
                    if isinstance(e, HTTPException):
                        raise e
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid or corrupted PDF file: {str(e)}"
                    )
                
                # Extract text from PDF using improved process_pdf function
                # This now first tries direct text extraction and only falls back to OCR if needed
                try:
                    extracted_text, confidence = await process_pdf(temp_file_path, ocr_method)
                    
                    if not extracted_text.strip():
                        print(f"[API] ⚠️ No text extracted from PDF: {file.filename}")
                except Exception as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f"PDF text extraction failed: {str(e)}"
                    )
                    
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"PDF processing failed: {str(e)}"
                )
            
        # Word document processing
        elif (content_type == 'application/msword' or 
              content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or
              file_ext.lower() in ['.doc', '.docx']):
            print(f"[API] Processing Word document: {file.filename}")
            
            try:
                # Extract text from Word document
                try:
                    extracted_text = docx2txt.process(temp_file_path)
                    confidence = 1.0  # Text extraction from Word has high confidence
                    
                    if not extracted_text.strip():
                        print(f"[API] ⚠️ No text extracted from Word document: {file.filename}")
                except Exception as e:
                    raise HTTPException(
                        status_code=422,
                        detail=f"Failed to extract text from Word document: {str(e)}"
                    )
                    
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Word document processing failed: {str(e)}"
                )
            
        else:
            # Unsupported file type (this should be caught by the earlier validation)
            os.remove(temp_file_path)
            raise HTTPException(
                status_code=415, 
                detail=f"Unsupported file type: {content_type or file_ext}"
            )
        
        # Check if we have any extracted text
        if not extracted_text:
            print(f"[API] ⚠️ No text extracted from document: {file.filename}")
            cleaned_text = ""
            language_detection = {
                "language_code": "unknown",
                "language_name": "Unknown",
                "confidence": 0.0,
                "is_kmrl_primary": False
            }
        else:
            # Clean extracted text
            try:
                cleaned_text = clean_extracted_text(extracted_text)
            except Exception as e:
                print(f"[API] ⚠️ Text cleaning error: {str(e)}. Using original text.")
                cleaned_text = extracted_text
            
            # Detect language
            try:
                language_detection = await detect_language(cleaned_text)
                
                if language_detection.get("language_code") == "unknown":
                    print(f"[API] ⚠️ Language detection failed for document: {file.filename}")
            except Exception as e:
                print(f"[API] ⚠️ Language detection error: {str(e)}")
                language_detection = {
                    "language_code": "unknown",
                    "language_name": "Unknown",
                    "confidence": 0.0,
                    "is_kmrl_primary": False
                }
        
        # Translation if requested
        translation_result = None
        if include_translation and cleaned_text:
            try:
                translation_result = await translate_text(
                    text=cleaned_text,
                    source_language=language_detection.get("language_code", "auto"),
                    target_language=target_language
                )
                
                if translation_result.get("error"):
                    print(f"[API] ⚠️ Translation warning: {translation_result.get('error')}")
            except Exception as e:
                print(f"[API] ⚠️ Translation error: {str(e)}")
                translation_result = {
                    "original_text": cleaned_text,
                    "translated_text": "",
                    "source_language": language_detection.get("language_code", "unknown"),
                    "target_language": target_language,
                    "source_language_name": language_detection.get("language_name", "Unknown"),
                    "target_language_name": target_language,
                    "error": f"Translation failed: {str(e)}"
                }
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Create result object
        result = {
            "ocr": {
                "text": cleaned_text,
                "confidence": confidence,
                "method": ocr_method,
                "processing_time_seconds": processing_time,
                "character_count": len(cleaned_text),
                "word_count": len(cleaned_text.split()) if cleaned_text else 0
            },
            "language_detection": language_detection,
            "translation": translation_result,
            "processing_info": {
                "processing_id": processing_id,
                "filename": file.filename,
                "file_type": content_type,
                "file_size": os.path.getsize(temp_file_path),
                "upload_timestamp": datetime.now().isoformat(),
                "processing_time_seconds": processing_time
            }
        }
        
        # Store result for later retrieval (temporary in-memory storage)
        processing_results[processing_id] = result
        
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        print(f"[API] ✅ Document processing completed in {processing_time:.2f} seconds (ID: {processing_id})")
        
        # Start background classification task if text was extracted
        if cleaned_text:
            background_tasks.add_task(
                prepare_classification_background,
                processing_id=processing_id,
                text=cleaned_text,
                translation=translation_result["translated_text"] if translation_result else None
            )
        
        # Return processing results
        return {
            "success": True,
            "message": "Document processed successfully",
            "data": result
        }
        
    except HTTPException as http_ex:
        # Clean up temp file if it exists
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as cleanup_error:
                print(f"[API] ⚠️ Failed to clean up temp file: {str(cleanup_error)}")
        
        error_msg = f"Document processing error: {http_ex.detail}"
        print(f"[API] ❌ {error_msg} [Status: {http_ex.status_code}]")
        
        raise http_ex
        
    except Exception as e:
        # Clean up temp file if it exists
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as cleanup_error:
                print(f"[API] ⚠️ Failed to clean up temp file: {str(cleanup_error)}")
        
        # Determine appropriate status code based on error type
        status_code = 500  # Default to internal server error
        
        if "insufficient permission" in str(e).lower() or "access denied" in str(e).lower():
            status_code = 403
        elif "not found" in str(e).lower():
            status_code = 404
        elif "timeout" in str(e).lower():
            status_code = 504
        
        error_msg = f"Document processing failed: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=status_code,
            detail=error_msg
        )

@router.post("/classify/{processing_id}")
async def classify_document(
    processing_id: str,
    text_data: dict
):
    """
    Classify document text based on content
    - Uses text from OCR or document extraction
    - Returns document category, department, priority
    """
    print(f"[API] Starting document classification (ID: {processing_id})")
    
    try:
        # Validate processing ID
        if not processing_id or not isinstance(processing_id, str) or len(processing_id) < 5:
            raise HTTPException(
                status_code=400,
                detail="Invalid processing ID format"
            )
        
        # Validate request body
        if not text_data:
            raise HTTPException(
                status_code=400,
                detail="Request body is required with 'text' field"
            )
        
        # Extract text and translation from request
        if not isinstance(text_data, dict):
            raise HTTPException(
                status_code=400,
                detail="Request body must be a JSON object with 'text' field"
            )
            
        text = text_data.get("text", "")
        translation = text_data.get("translation")
        
        # Validate text content
        if not text or not isinstance(text, str) or not text.strip():
            raise HTTPException(
                status_code=400, 
                detail="Text content is required for classification and cannot be empty"
            )
            
        if len(text) > 100000:  # Limit text size for classification
            print(f"[API] ⚠️ Text too long for classification, truncating: {len(text)} chars")
            text = text[:100000]
        
        # Use translated text if available (better for non-English documents)
        if translation and isinstance(translation, str) and translation.strip():
            classification_text = translation
            text_source = "translation"
        else:
            classification_text = text
            text_source = "original"
        
        print(f"[API] Using {text_source} text for classification (length: {len(classification_text)} chars)")
        
        try:
            # Classify document (not async)
            classification_result = classification_service.classify_document(classification_text)
            
            # Validate classification result
            if not classification_result:
                raise ValueError("Classification returned empty result")
                
            if "category" not in classification_result:
                print("[API] ⚠️ Classification returned empty category")
                classification_result["category"] = "Unknown"
                classification_result["confidence"] = 0.0
            
            print(f"[API] ✅ Classification completed (ID: {processing_id}): {classification_result['category']}")
            
            # Return classification results
            return {
                "success": True,
                "message": "Document classified successfully",
                "data": {
                    "processing_id": processing_id,
                    "classification": classification_result,
                    "text_source": text_source
                }
            }
        except Exception as classify_error:
            print(f"[API] ❌ Classification service error: {str(classify_error)}")
            raise HTTPException(
                status_code=422,
                detail=f"Classification service error: {str(classify_error)}"
            )
        
    except HTTPException:
        # Pass through HTTP exceptions
        raise
    
    except ValueError as ve:
        # Handle value errors (validation errors)
        error_msg = f"Classification validation error: {str(ve)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=400,
            detail=error_msg
        )
        
    except Exception as e:
        # Handle unexpected errors
        error_msg = f"Classification failed: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

# Helper function to detect language
async def detect_language(text: str):
    """Detect language of text"""
    try:
        # Validate input
        if not text or not text.strip():
            print("[API] ⚠️ Empty text provided for language detection")
            return {
                "language_code": "unknown",
                "language_name": "Unknown",
                "confidence": 0.0,
                "is_kmrl_primary": False
            }
        
        # Limit text length for processing efficiency
        if len(text) > 5000:
            detection_text = text[:5000]  # Use first 5000 chars for detection
        else:
            detection_text = text
            
        # TODO: Implement real language detection
        # For demo, assume English with Malayalam detection logic
        
        # Simple detection - check for Malayalam unicode range
        try:
            malayalam_chars = sum(1 for char in detection_text if '\u0D00' <= char <= '\u0D7F')
            total_chars = len(detection_text.strip())
            
            if total_chars == 0:
                raise ValueError("No valid characters for language detection")
                
            malayalam_ratio = malayalam_chars / total_chars
            is_malayalam = malayalam_ratio > 0.3  # If >30% chars are Malayalam
            
            if is_malayalam:
                return {
                    "language_code": "ml",
                    "language_name": "Malayalam",
                    "confidence": min(0.95, 0.5 + malayalam_ratio),  # Adjust confidence based on ratio
                    "is_kmrl_primary": True
                }
            else:
                return {
                    "language_code": "en",
                    "language_name": "English",
                    "confidence": 0.95,
                    "is_kmrl_primary": True
                }
        except Exception as char_error:
            print(f"[API] ⚠️ Character analysis error: {str(char_error)}")
            raise
            
    except Exception as e:
        print(f"[API] ⚠️ Language detection error: {str(e)}")
        # Return unknown language if detection completely fails
        return {
            "language_code": "unknown",
            "language_name": "Unknown",
            "confidence": 0.0,
            "is_kmrl_primary": False
        }

# Helper function to translate text
async def translate_text(text: str, source_language: str, target_language: str):
    """Translate text to target language"""
    try:
        # Validate input
        if not text or not text.strip():
            return {
                "original_text": text,
                "translated_text": "",
                "source_language": source_language or "unknown",
                "target_language": target_language,
                "source_language_name": source_language or "Unknown",
                "target_language_name": target_language or "Unknown",
                "error": "Empty text provided for translation"
            }
        
        if not target_language:
            return {
                "original_text": text,
                "translated_text": "",
                "source_language": source_language or "unknown",
                "target_language": "unknown",
                "source_language_name": source_language or "Unknown",
                "target_language_name": "Unknown",
                "error": "No target language specified"
            }
        
        # Limit text length for translation efficiency
        if len(text) > 10000:
            translation_text = text[:10000]  # Use first 10000 chars for translation
            truncated = True
        else:
            translation_text = text
            truncated = False
            
        # TODO: Implement real translation service
        # For demo, return mock translation
        
        # Only translate if source is different from target
        if source_language == "unknown":
            return {
                "original_text": text,
                "translated_text": "",
                "source_language": "unknown",
                "target_language": target_language,
                "source_language_name": "Unknown",
                "target_language_name": "English" if target_language == "en" else target_language,
                "error": "Source language could not be determined for translation"
            }
        
        if source_language != target_language and source_language == "ml":
            print(f"[API] Translating text from {source_language} to {target_language}")
            
            try:
                # Use the real translation service
                from services.translation_service import TranslationService
                
                # Create a translation service instance
                translation_service = TranslationService()
                
                # Perform the real translation
                translation_result = translation_service.translate_text(
                    translation_text,
                    target_language=target_language,
                    source_language=source_language
                )
                
                error_msg = "Text was truncated for translation (10000 char limit)" if truncated else None
                if translation_result.error:
                    error_msg = translation_result.error if not error_msg else f"{error_msg}; {translation_result.error}"
                
                return {
                    "original_text": text,
                    "translated_text": translation_result.translated_text,
                    "source_language": translation_result.source_language,
                    "target_language": translation_result.target_language,
                    "source_language_name": translation_result.source_language_name,
                    "target_language_name": translation_result.target_language_name,
                    "error": error_msg
                }
            except Exception as translation_error:
                print(f"[API] ⚠️ Translation service error: {str(translation_error)}")
                return {
                    "original_text": text,
                    "translated_text": "",
                    "source_language": source_language,
                    "target_language": target_language,
                    "source_language_name": "Malayalam",
                    "target_language_name": "English",
                    "error": f"Translation service error: {str(translation_error)}"
                }
        else:
            # No translation needed or supported
            if source_language == target_language:
                message = "Source and target languages are the same, no translation needed"
            else:
                message = f"Translation from {source_language} to {target_language} not supported"
                
            return {
                "original_text": text,
                "translated_text": text if source_language == target_language else "",
                "source_language": source_language,
                "target_language": target_language,
                "source_language_name": "English" if source_language == "en" else source_language,
                "target_language_name": "English" if target_language == "en" else target_language,
                "error": None if source_language == target_language else message
            }
    except Exception as e:
        print(f"[API] ❌ Translation error: {str(e)}")
        return {
            "original_text": text,
            "translated_text": "",
            "source_language": source_language or "unknown",
            "target_language": target_language or "unknown",
            "source_language_name": source_language or "Unknown",
            "target_language_name": target_language or "Unknown",
            "error": f"Translation failed: {str(e)}"
        }

# Helper function to process PDF files
async def process_pdf(pdf_path: str, ocr_method: str):
    """
    Process PDF file for text extraction
    - Directly extracts text from PDF using PyPDF2 (faster and more accurate)
    - Falls back to OCR only if direct extraction yields no text (for scanned PDFs)
    """
    try:
        print(f"[API] Processing PDF: {pdf_path}")
        
        # Verify file exists
        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        # Check file size
        file_size = os.path.getsize(pdf_path)
        if file_size > 50 * 1024 * 1024:  # 50MB
            raise ValueError(f"PDF file too large: {file_size / (1024 * 1024):.1f} MB (max: 50MB)")
        
        # Try direct text extraction first (more efficient)
        extracted_text = ""
        processed_pages = 0
        
        try:
            # Open PDF using PyPDF2
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                page_count = len(pdf_reader.pages)
                
                if page_count == 0:
                    raise ValueError("PDF contains no pages")
                if page_count > 50:
                    raise ValueError(f"PDF contains too many pages: {page_count} (max: 50)")
                    
                print(f"[API] PDF has {page_count} pages")
                
                # Extract text from each page
                all_text = []
                
                for page_num in range(page_count):
                    try:
                        page_text = pdf_reader.pages[page_num].extract_text() or ""
                        if page_text.strip():
                            all_text.append(page_text)
                            processed_pages += 1
                            print(f"[API] Extracted text from page {page_num + 1}/{page_count} - {len(page_text)} chars")
                        else:
                            print(f"[API] No text extracted from page {page_num + 1}/{page_count}")
                    except Exception as e:
                        print(f"[API] ⚠️ Error extracting text from PDF page {page_num + 1}: {str(e)}. Skipping page.")
                
                extracted_text = "\n\n".join(all_text)
        except Exception as e:
            print(f"[API] ⚠️ Error in direct PDF text extraction: {str(e)}")
            extracted_text = ""
        
        # If direct extraction yielded no text, the PDF might be scanned (image-based)
        # Only then fall back to OCR
        if not extracted_text.strip():
            print("[API] No text extracted directly from PDF. PDF may be scanned/image-based. Falling back to OCR...")
            
            # Fall back to OCR for scanned PDFs
            try:
                # Load PDF document for OCR processing
                pdf = pdfium.PdfDocument(pdf_path)
                page_count = len(pdf)
                
                # Reset counters
                all_text = []
                total_confidence = 0.0
                processed_pages = 0
                
                for page_num in range(page_count):
                    try:
                        # Render page to image
                        page = pdf.get_page(page_num)
                        bitmap = page.render(scale=2.0, rotation=0, crop=(0, 0, 0, 0))
                        pil_image = bitmap.to_pil()
                        
                        # Save image to bytes for OCR
                        img_byte_arr = io.BytesIO()
                        pil_image.save(img_byte_arr, format='PNG')
                        img_bytes = img_byte_arr.getvalue()
                        
                        # Extract text using OCR
                        ocr_result = await vision_service.extract_text_async(img_bytes, method=ocr_method)
                        
                        if ocr_result.text:
                            all_text.append(ocr_result.text)
                            total_confidence += ocr_result.confidence
                            processed_pages += 1
                            print(f"[API] OCR processed page {page_num + 1}/{page_count} - {len(ocr_result.text)} chars")
                    except Exception as e:
                        print(f"[API] ⚠️ Error in OCR processing of PDF page {page_num + 1}: {str(e)}. Skipping page.")
                
                if processed_pages > 0:
                    extracted_text = "\n\n".join(all_text)
                    avg_confidence = total_confidence / processed_pages
                    print(f"[API] ✅ OCR fallback processing complete: {processed_pages}/{page_count} pages processed")
                    return extracted_text, avg_confidence
            except Exception as e:
                print(f"[API] ❌ OCR fallback processing failed: {str(e)}")
        
        # Check if we got any text
        if not extracted_text.strip():
            raise ValueError("Could not extract any text from the PDF")
        
        print(f"[API] ✅ PDF processing complete: {processed_pages}/{page_count} pages processed")
        
        # Direct text extraction has high confidence
        return extracted_text, 1.0
        
    except ValueError as ve:
        # Value errors are user-related issues with the PDF
        print(f"[API] ❌ PDF validation error: {str(ve)}")
        raise ValueError(str(ve))
        
    except FileNotFoundError as fnf:
        # File not found is a system issue
        print(f"[API] ❌ PDF file error: {str(fnf)}")
        raise ValueError(f"PDF file error: {str(fnf)}")
        
    except Exception as e:
        # General processing errors
        print(f"[API] ❌ PDF processing error: {str(e)}")
        raise ValueError(f"PDF processing failed: {str(e)}")

# Background task for classification preparation
async def prepare_classification_background(processing_id: str, text: str, translation: Optional[str] = None):
    """Background task to prepare document for classification"""
    print(f"[API] Background classification task started for {processing_id}")
    
    try:
        # Validate input
        if not processing_id:
            print("[API] ❌ No processing ID provided for classification task")
            return
            
        if not text or not text.strip():
            print(f"[API] ⚠️ No text content provided for classification task (ID: {processing_id})")
            # Still record the task but mark as empty
            if processing_id in processing_results:
                processing_results[processing_id]["classification_ready"] = {
                    "text": "",
                    "translation": "",
                    "error": "No text content available for classification"
                }
            return
        
        # In a real implementation, this would queue the document for classification
        # or store it in a database for later processing
        
        # For demo purposes, we're just storing the text for later classification
        if processing_id in processing_results:
            # Store sanitized content
            processing_results[processing_id]["classification_ready"] = {
                "text": text[:50000] if text else "",  # Limit text size
                "translation": translation[:50000] if translation else None,
                "timestamp": datetime.now().isoformat(),
                "error": None
            }
            
            print(f"[API] ✅ Document {processing_id} ready for classification")
        else:
            print(f"[API] ⚠️ Processing result not found for ID: {processing_id}")
            
    except Exception as e:
        print(f"[API] ❌ Background classification task error: {str(e)}")
        
        # Record the error
        try:
            if processing_id in processing_results:
                processing_results[processing_id]["classification_ready"] = {
                    "text": text[:100] + "..." if text and len(text) > 100 else text,
                    "translation": None,
                    "timestamp": datetime.now().isoformat(),
                    "error": f"Classification preparation failed: {str(e)}"
                }
        except Exception as record_error:
            print(f"[API] ❌ Failed to record classification error: {str(record_error)}")
