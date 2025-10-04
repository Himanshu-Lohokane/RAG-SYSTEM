# DataTrack KMRL - Entity Extraction Endpoints
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Optional, Dict, List, Any
import json
import time

# Add imports for entity extraction service
from services.extraction_service import EntityExtractionService

# Initialize router
router = APIRouter(prefix="/api/extract", tags=["entity-extraction"])

# Initialize services
extraction_service = EntityExtractionService()

@router.post("/entities")
async def extract_entities(
    text: str,
    language: str = "en",
    entities: Optional[List[str]] = None
):
    """
    Extract entities from text
    - Extracts names, organizations, locations, etc.
    - Optimized for technical and administrative documents
    
    Args:
        text: The text to analyze
        language: Language code (en, ml)
        entities: Optional list of entity types to extract
    """
    start_time = time.time()
    
    try:
        # Validate text input
        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text content is required and cannot be empty"
            )
            
        if len(text) > 100000:  # Limit text size to avoid processing very large texts
            print(f"[API] ⚠️ Text too long for entity extraction, truncating: {len(text)} chars")
            text = text[:100000]
            
        print(f"[API] Entity extraction request - Text length: {len(text)} chars")
        
        # Validate language code
        supported_languages = ["en", "ml", "hi", "ta"]
        if language not in supported_languages:
            print(f"[API] ⚠️ Unsupported language: {language}, defaulting to English")
            language = "en"
        
        # Default entity types if not specified
        if not entities:
            entities = ["PERSON", "ORGANIZATION", "LOCATION", "DATE", "NUMBER"]
        elif not isinstance(entities, list):
            raise HTTPException(
                status_code=400,
                detail="Entities must be provided as a list of strings"
            )
            
        # Extract entities
        try:
            entities_result = extraction_service.extract_entities(text, language)
        except ValueError as ve:
            raise HTTPException(status_code=422, detail=f"Entity extraction validation error: {str(ve)}")
        except NotImplementedError as nie:
            raise HTTPException(status_code=501, detail=f"Entity extraction not supported: {str(nie)}")
            
        if not entities_result or not entities_result.entities:
            print("[API] ⚠️ No entities found in text")
            
        processing_time = time.time() - start_time
        print(f"[API] ✅ Entity extraction completed in {processing_time:.2f}s")
        
        return {
            "success": True,
            "message": f"Successfully extracted {len(entities_result.entities)} entities",
            "data": entities_result.dict(),
            "processing_time_seconds": round(processing_time, 3),
            "language": language
        }
        
    except HTTPException:
        # Pass through HTTP exceptions
        raise
        
    except ValueError as ve:
        error_msg = f"Entity extraction validation error: {str(ve)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=400,
            detail=error_msg
        )
        
    except Exception as e:
        error_msg = f"Entity extraction failed: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

@router.post("/key-value-pairs")
async def extract_key_value_pairs(
    text: str,
    language: str = "en"
):
    """
    Extract key-value pairs from text
    - Useful for forms, invoices, technical documents
    - Extracts structured data like field:value pairs
    
    Args:
        text: The text to analyze
        language: Language code (en, ml)
    """
    start_time = time.time()
    
    try:
        # Validate text input
        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text content is required and cannot be empty"
            )
            
        if len(text) > 50000:  # Limit text size
            print(f"[API] ⚠️ Text too long for key-value extraction, truncating: {len(text)} chars")
            text = text[:50000]
            
        print(f"[API] Key-value extraction request - Text length: {len(text)} chars")
        
        # Validate language code
        supported_languages = ["en", "ml", "hi", "ta"]
        if language not in supported_languages:
            print(f"[API] ⚠️ Unsupported language: {language}, defaulting to English")
            language = "en"
            
        # Extract key-value pairs
        try:
            kv_result = extraction_service.extract_key_value_pairs(text, language)
            
            # Check if result is valid
            if not kv_result:
                raise ValueError("Key-value extraction returned empty result")
                
            if not kv_result.pairs:
                print("[API] ⚠️ No key-value pairs found in text")
                
        except ValueError as ve:
            raise HTTPException(status_code=422, detail=f"Key-value extraction error: {str(ve)}")
        except NotImplementedError as nie:
            raise HTTPException(status_code=501, detail=f"Key-value extraction not supported: {str(nie)}")
        
        processing_time = time.time() - start_time
        print(f"[API] ✅ Key-value extraction completed in {processing_time:.2f}s")
        
        return {
            "success": True,
            "message": f"Successfully extracted {len(kv_result.pairs)} key-value pairs",
            "data": kv_result.dict(),
            "processing_time_seconds": round(processing_time, 3),
            "language": language
        }
        
    except HTTPException:
        # Pass through HTTP exceptions
        raise
        
    except ValueError as ve:
        error_msg = f"Key-value extraction validation error: {str(ve)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=400,
            detail=error_msg
        )
        
    except Exception as e:
        error_msg = f"Key-value extraction failed: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

@router.post("/tables")
async def extract_tables(
    file: UploadFile = File(...),
    include_table_text: bool = Form(True),
    include_raw_data: bool = Form(False)
):
    """
    Extract tables from document images
    - Works for structured reports, financial documents, etc.
    - Returns table data in structured format
    
    Args:
        file: Document image containing tables
        include_table_text: Include raw text from tables
        include_raw_data: Include raw detection data
    """
    start_time = time.time()
    
    try:
        # Validate file exists
        if not file:
            raise HTTPException(
                status_code=400,
                detail="File is required"
            )
            
        # Validate filename
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="File must have a filename"
            )
            
        print(f"[API] Table extraction request - File: {file.filename}")
        
        # Validate content type
        content_type = file.content_type or ""
        supported_types = ["image/jpeg", "image/png", "image/tiff", "application/pdf"]
        
        if not any(supported_type in content_type.lower() for supported_type in supported_types):
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type: {content_type}. Supported types: JPEG, PNG, TIFF, PDF"
            )
            
        try:
            # Read file data with size limit (10MB)
            file_data = await file.read()
            
            if len(file_data) > 10 * 1024 * 1024:  # 10MB
                raise HTTPException(
                    status_code=413,
                    detail="File too large. Maximum size is 10MB"
                )
                
            if len(file_data) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="File is empty"
                )
                
            # Extract tables from image
            try:
                tables_result = extraction_service.extract_tables(file_data)
            except ValueError as ve:
                raise HTTPException(status_code=422, detail=f"Table extraction validation error: {str(ve)}")
            except NotImplementedError as nie:
                raise HTTPException(status_code=501, detail=f"Table extraction not supported: {str(nie)}")
            
            # Check if any tables were found
            if not tables_result or not tables_result.tables or len(tables_result.tables) == 0:
                print("[API] ⚠️ No tables found in the document")
                return {
                    "success": True,
                    "message": "No tables found in the document",
                    "data": {"tables": []},
                    "processing_time_seconds": round(time.time() - start_time, 3)
                }
                
            # Prepare response data
            tables_data = tables_result.dict()
            
            # Remove raw data if not requested
            if not include_raw_data and "raw_data" in tables_data:
                del tables_data["raw_data"]
                
            # Remove table text if not requested
            if not include_table_text:
                for table in tables_data.get("tables", []):
                    if "text" in table:
                        del table["text"]
                        
            processing_time = time.time() - start_time
            print(f"[API] ✅ Table extraction completed in {processing_time:.2f}s - Found {len(tables_data.get('tables', []))} tables")
            
            return {
                "success": True,
                "message": f"Successfully extracted {len(tables_data.get('tables', []))} tables",
                "data": tables_data,
                "processing_time_seconds": round(processing_time, 3),
                "file_info": {
                    "filename": file.filename,
                    "content_type": content_type,
                    "size_bytes": len(file_data)
                }
            }
        
        except HTTPException:
            # Pass through HTTP exceptions
            raise
            
        finally:
            # Ensure file is closed
            file.file.close()
            
    except HTTPException:
        # Pass through HTTP exceptions
        raise
        
    except ValueError as ve:
        error_msg = f"Table extraction validation error: {str(ve)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=400,
            detail=error_msg
        )
        
    except Exception as e:
        error_msg = f"Table extraction failed: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

@router.post("/forms")
async def extract_form_fields(
    file: UploadFile = File(...),
    form_template: Optional[str] = Form(None)
):
    """
    Extract form fields from document images
    - Works for forms, applications, structured documents
    - Can use templates for known form types
    
    Args:
        file: Document image containing form fields
        form_template: Optional template name for known form types
    """
    start_time = time.time()
    
    try:
        # Validate file exists
        if not file:
            raise HTTPException(
                status_code=400,
                detail="File is required"
            )
            
        # Validate filename
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="File must have a filename"
            )
            
        print(f"[API] Form extraction request - File: {file.filename}")
        
        # Validate content type
        content_type = file.content_type or ""
        supported_types = ["image/jpeg", "image/png", "image/tiff", "application/pdf"]
        
        if not any(supported_type in content_type.lower() for supported_type in supported_types):
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type: {content_type}. Supported types: JPEG, PNG, TIFF, PDF"
            )
            
        # Validate form template if provided
        if form_template and not isinstance(form_template, str):
            raise HTTPException(
                status_code=400,
                detail="Form template must be a string"
            )
            
        try:
            # Read file data with size limit (10MB)
            file_data = await file.read()
            
            if len(file_data) > 10 * 1024 * 1024:  # 10MB
                raise HTTPException(
                    status_code=413,
                    detail="File too large. Maximum size is 10MB"
                )
                
            if len(file_data) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="File is empty"
                )
                
            # Validate and process form template
            if form_template:
                print(f"[API] Using form template: {form_template}")
                # You could add validation for supported templates here
                
            # Extract form fields
            try:
                form_result = extraction_service.extract_form_fields(file_data, form_template)
            except ValueError as ve:
                raise HTTPException(status_code=422, detail=f"Form extraction validation error: {str(ve)}")
            except NotImplementedError as nie:
                raise HTTPException(status_code=501, detail=f"Form extraction not supported: {str(nie)}")
            
            # Check if any fields were extracted
            if not form_result or not form_result.fields or len(form_result.fields) == 0:
                print("[API] ⚠️ No form fields found in the document")
                return {
                    "success": True,
                    "message": "No form fields found in the document",
                    "data": {"fields": []},
                    "processing_time_seconds": round(time.time() - start_time, 3)
                }
                
            processing_time = time.time() - start_time
            print(f"[API] ✅ Form extraction completed in {processing_time:.2f}s - Found {len(form_result.fields)} fields")
            
            return {
                "success": True,
                "message": f"Successfully extracted {len(form_result.fields)} form fields",
                "data": form_result.dict(),
                "processing_time_seconds": round(processing_time, 3),
                "template_used": form_template,
                "file_info": {
                    "filename": file.filename,
                    "content_type": content_type,
                    "size_bytes": len(file_data)
                }
            }
        
        except HTTPException:
            # Pass through HTTP exceptions
            raise
            
        finally:
            # Ensure file is closed
            file.file.close()
            
    except HTTPException:
        # Pass through HTTP exceptions
        raise
        
    except ValueError as ve:
        error_msg = f"Form extraction validation error: {str(ve)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=400,
            detail=error_msg
        )
        
    except Exception as e:
        error_msg = f"Form extraction failed: {str(e)}"
        print(f"[API] ❌ {error_msg}")
        
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )
