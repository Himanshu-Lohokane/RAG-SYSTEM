# DataTrack KMRL - OCR Data Models
# Type-safe data structures for document processing
# Supports images, PDFs, and Word documents

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class OCRResult:
    """Result from OCR text extraction - KMRL Document Processing"""
    text: str
    confidence: float
    method: str  # 'document', 'text', 'pdf', or 'docx'
    error: Optional[str] = None
    character_count: Optional[int] = None
    word_count: Optional[int] = None
    
    def __post_init__(self):
        """Calculate character and word counts if not provided"""
        if self.character_count is None:
            self.character_count = len(self.text) if self.text else 0
        
        if self.word_count is None:
            self.word_count = len(self.text.split()) if self.text else 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'text': self.text,
            'confidence': self.confidence,
            'method': self.method,
            'error': self.error,
            'character_count': self.character_count,
            'word_count': self.word_count
        }

@dataclass
class LanguageDetectionResult:
    """Result from language detection - Supporting English/Malayalam for KMRL"""
    language_code: str
    language_name: str
    confidence: float
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'language_code': self.language_code,
            'language_name': self.language_name,
            'confidence': self.confidence,
            'error': self.error
        }

@dataclass
class TranslationResult:
    """Result from text translation - KMRL Multilingual Support"""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    source_language_name: str
    target_language_name: str
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'original_text': self.original_text,
            'translated_text': self.translated_text,
            'source_language': self.source_language,
            'target_language': self.target_language,
            'source_language_name': self.source_language_name,
            'target_language_name': self.target_language_name,
            'error': self.error
        }

@dataclass
class DocumentClassificationResult:
    """Result from document classification - KMRL Document Categories"""
    category: str
    category_name: str
    confidence: float
    department: Optional[str] = None
    priority: Optional[str] = None  # high, medium, low
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'category': self.category,
            'category_name': self.category_name,
            'confidence': self.confidence,
            'department': self.department,
            'priority': self.priority,
            'error': self.error
        }

@dataclass
class KMRLDocumentProcessingResult:
    """Complete document processing result for KMRL workflow"""
    # Input metadata
    filename: str
    file_size: int
    upload_timestamp: str
    processing_id: str
    
    # OCR Results
    ocr_result: OCRResult
    
    # Language Detection (for Malayalam/English detection)
    language_detection: LanguageDetectionResult
    
    # Translation Results (Optional - when needed)
    translation_result: Optional[TranslationResult] = None
    
    # Classification Results (Future enhancement)
    classification_result: Optional[DocumentClassificationResult] = None
    
    # Processing metadata
    processing_time_seconds: Optional[float] = None
    success: bool = True
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'processing_info': {
                'filename': self.filename,
                'file_size': self.file_size,
                'upload_timestamp': self.upload_timestamp,
                'processing_id': self.processing_id,
                'processing_time_seconds': self.processing_time_seconds,
                'success': self.success,
                'errors': self.errors
            },
            'ocr': self.ocr_result.to_dict() if self.ocr_result else None,
            'language_detection': self.language_detection.to_dict() if self.language_detection else None,
            'translation': self.translation_result.to_dict() if self.translation_result else None,
            'classification': self.classification_result.to_dict() if self.classification_result else None
        }

@dataclass
class BatchProcessingResult:
    """Result from batch processing multiple KMRL documents"""
    total_documents: int
    successful: int
    failed: int
    results: List[KMRLDocumentProcessingResult]
    processing_errors: List[str]
    batch_id: str
    batch_timestamp: str
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_documents == 0:
            return 0.0
        return (self.successful / self.total_documents) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'batch_info': {
                'batch_id': self.batch_id,
                'batch_timestamp': self.batch_timestamp,
                'total_documents': self.total_documents,
                'successful': self.successful,
                'failed': self.failed,
                'success_rate': self.success_rate,
                'processing_errors': self.processing_errors
            },
            'results': [result.to_dict() for result in self.results]
        }