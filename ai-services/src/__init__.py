# DataTrack KMRL - AI Services Package
# OCR and Document Processing Services

from .services.ocr_service import VisionService
from .services.translation_service import TranslationService
from .models.ocr_models import (
    OCRResult,
    LanguageDetectionResult,
    TranslationResult,
    DocumentClassificationResult,
    KMRLDocumentProcessingResult,
    BatchProcessingResult
)
from .config.settings import Config

__version__ = "1.0.0"
__description__ = "AI-powered document processing for KMRL Metro Rail"

__all__ = [
    # Services
    'VisionService',
    'TranslationService',
    
    # Models
    'OCRResult',
    'LanguageDetectionResult', 
    'TranslationResult',
    'DocumentClassificationResult',
    'KMRLDocumentProcessingResult',
    'BatchProcessingResult',
    
    # Configuration
    'Config'
]