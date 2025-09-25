# DataTrack KMRL - Image Preprocessing
# Optimize images for better OCR performance

import os
import sys
import asyncio
import io
from typing import Union, List, Optional, Dict, Any
from PIL import Image, ImageEnhance, ImageFilter

async def preprocess_image(image_path: Union[str, bytes]) -> bytes:
    """
    Preprocess image to improve OCR quality
    
    Args:
        image_path: Path to image file or image bytes
        
    Returns:
        Preprocessed image bytes
    """
    try:
        # Open image from file or bytes
        if isinstance(image_path, str):
            image = Image.open(image_path)
        else:
            image = Image.open(io.BytesIO(image_path))
        
        # Convert to RGB if needed (some documents have alpha channel)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large (but maintain quality for OCR)
        max_dimension = 3000
        width, height = image.size
        if width > max_dimension or height > max_dimension:
            scale = max_dimension / max(width, height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.3)
        
        # Convert to bytes
        output = io.BytesIO()
        image.save(output, format='PNG')
        
        return output.getvalue()
        
    except Exception as e:
        print(f"[PREPROCESS] ❌ Image preprocessing failed: {str(e)}")
        # If preprocessing fails, return original image
        if isinstance(image_path, str):
            with open(image_path, 'rb') as f:
                return f.read()
        else:
            return image_path

async def optimize_for_ocr(image_path: Union[str, bytes], enhance_text: bool = True) -> bytes:
    """
    Optimize image specifically for text extraction
    
    Args:
        image_path: Path to image file or image bytes
        enhance_text: Whether to apply additional text enhancement
        
    Returns:
        Optimized image bytes
    """
    try:
        # Open image
        if isinstance(image_path, str):
            image = Image.open(image_path)
        else:
            image = Image.open(io.BytesIO(image_path))
        
        # Convert to grayscale for better OCR
        image = image.convert('L')
        
        # Apply some sharpening for text clarity
        image = image.filter(ImageFilter.SHARPEN)
        
        if enhance_text:
            # Binarize the image (convert to black and white)
            # This can help with text clarity for OCR
            threshold = 150  # Adjust based on image brightness
            image = image.point(lambda p: 255 if p > threshold else 0)
        
        # Convert to bytes
        output = io.BytesIO()
        image.save(output, format='PNG')
        
        return output.getvalue()
        
    except Exception as e:
        print(f"[PREPROCESS] ❌ OCR optimization failed: {str(e)}")
        # If optimization fails, return original image
        if isinstance(image_path, str):
            with open(image_path, 'rb') as f:
                return f.read()
        else:
            return image_path

async def preprocess_document_image(image_path: Union[str, bytes], document_type: str = 'general') -> bytes:
    """
    Preprocess document image based on document type
    
    Args:
        image_path: Path to image file or image bytes
        document_type: Type of document ('general', 'form', 'id_card', 'invoice')
        
    Returns:
        Preprocessed image bytes
    """
    try:
        # Open image
        if isinstance(image_path, str):
            image = Image.open(image_path)
        else:
            image = Image.open(io.BytesIO(image_path))
        
        # Base processing for all document types
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Type-specific processing
        if document_type == 'form':
            # Forms need higher contrast and sharpness
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.7)
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)
            
        elif document_type == 'id_card':
            # ID cards often need more brightness and contrast
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.4)
            
        elif document_type == 'invoice':
            # Invoices often have table structures
            # Sharpen and increase contrast slightly
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.3)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            
        else:  # General document
            # General enhancement for readability
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.3)
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.2)
        
        # Convert to bytes
        output = io.BytesIO()
        image.save(output, format='PNG')
        
        return output.getvalue()
        
    except Exception as e:
        print(f"[PREPROCESS] ❌ Document preprocessing failed: {str(e)}")
        # If preprocessing fails, return original image
        if isinstance(image_path, str):
            with open(image_path, 'rb') as f:
                return f.read()
        else:
            return image_path
