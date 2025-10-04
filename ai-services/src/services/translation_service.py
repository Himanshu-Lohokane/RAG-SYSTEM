# DataTrack KMRL - Translation Service
# Google Cloud Translation API for English/Malayalam support

import sys
import os
from typing import Optional, List, Dict, Any
from google.cloud import translate_v2 as translate

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config
from models.ocr_models import LanguageDetectionResult, TranslationResult

class TranslationService:
    """Google Cloud Translation API service for KMRL multilingual support"""
    
    def __init__(self):
        """Initialize Translation client for English/Malayalam processing"""
        print("[TRANSLATION] Initializing Google Cloud Translation service for DataTrack-KMRL...")
        self.client = Config.get_translate_client()
        print("[TRANSLATION] ✅ Translation service ready for English/Malayalam processing")
    
    def detect_language(self, text: str) -> LanguageDetectionResult:
        """
        Detect language of text - Optimized for KMRL English/Malayalam documents
        
        Args:
            text: Text to analyze for language
            
        Returns:
            LanguageDetectionResult with detected language info
        """
        print(f"[TRANSLATION] Detecting language for text (length: {len(text)} chars)")
        
        try:
            # Use only first 1000 chars for language detection (API limit + efficiency)
            sample_text = text[:1000] if len(text) > 1000 else text
            
            result = self.client.detect_language(sample_text)
            
            language_code = result['language']
            confidence = result.get('confidence', 0.0)
            language_name = Config.get_language_name(language_code)
            
            print(f"[TRANSLATION] ✅ Language detected: {language_name} ({language_code}) - Confidence: {confidence:.2f}")
            
            # Special handling for KMRL primary languages
            if language_code in ['en', 'ml']:
                print(f"[TRANSLATION] 🎯 KMRL primary language detected: {language_name}")
            
            return LanguageDetectionResult(
                language_code=language_code,
                language_name=language_name,
                confidence=confidence,
                error=None
            )
            
        except Exception as e:
            error_msg = f"Language detection failed: {str(e)}"
            print(f"[TRANSLATION] ❌ {error_msg}")
            return LanguageDetectionResult(
                language_code="unknown",
                language_name="Unknown",
                confidence=0.0,
                error=error_msg
            )
    
    def translate_text(self, 
                      text: str, 
                      target_language: str = 'en',
                      source_language: Optional[str] = None) -> TranslationResult:
        """
        Translate text - Focused on KMRL Malayalam ↔ English translation
        
        Args:
            text: Text to translate
            target_language: Target language code (default: 'en')
            source_language: Source language code (auto-detect if None)
            
        Returns:
            TranslationResult with translation details
        """
        print(f"[TRANSLATION] Translating text to {target_language} (length: {len(text)} chars)")
        
        try:
            # Auto-detect source language if not provided
            if source_language is None:
                detection = self.detect_language(text)
                if detection.error:
                    return TranslationResult(
                        original_text=text,
                        translated_text="",
                        source_language="unknown",
                        target_language=target_language,
                        source_language_name="Unknown",
                        target_language_name=Config.get_language_name(target_language),
                        error=f"Could not detect source language: {detection.error}"
                    )
                source_language = detection.language_code
                print(f"[TRANSLATION] Auto-detected source language: {detection.language_name}")
            
            # Skip translation if source and target are the same
            if source_language == target_language:
                print(f"[TRANSLATION] ⚠️ Source and target languages are the same ({source_language}), skipping translation")
                return TranslationResult(
                    original_text=text,
                    translated_text=text,
                    source_language=source_language,
                    target_language=target_language,
                    source_language_name=Config.get_language_name(source_language),
                    target_language_name=Config.get_language_name(target_language),
                    error=None
                )
            
            # Perform translation
            result = self.client.translate(
                text,
                target_language=target_language,
                source_language=source_language,
                format_='text'
            )
            
            translated_text = result['translatedText']
            detected_source = result.get('detectedSourceLanguage', source_language)
            
            print(f"[TRANSLATION] ✅ Translation completed:")
            print(f"[TRANSLATION]   - From: {Config.get_language_name(detected_source)}")
            print(f"[TRANSLATION]   - To: {Config.get_language_name(target_language)}")
            print(f"[TRANSLATION]   - Original length: {len(text)} chars")
            print(f"[TRANSLATION]   - Translated length: {len(translated_text)} chars")
            
            # Special logging for KMRL language pairs
            if (detected_source == 'ml' and target_language == 'en') or \
               (detected_source == 'en' and target_language == 'ml'):
                print(f"[TRANSLATION] 🎯 KMRL primary language pair processed: {detected_source} → {target_language}")
            
            return TranslationResult(
                original_text=text,
                translated_text=translated_text,
                source_language=detected_source,
                target_language=target_language,
                source_language_name=Config.get_language_name(detected_source),
                target_language_name=Config.get_language_name(target_language),
                error=None
            )
            
        except Exception as e:
            error_msg = f"Translation failed: {str(e)}"
            print(f"[TRANSLATION] ❌ {error_msg}")
            return TranslationResult(
                original_text=text,
                translated_text="",
                source_language=source_language or "unknown",
                target_language=target_language,
                source_language_name=Config.get_language_name(source_language) if source_language else "Unknown",
                target_language_name=Config.get_language_name(target_language),
                error=error_msg
            )
    
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """
        Get list of supported languages with focus on KMRL relevant languages
        
        Returns:
            List of language dictionaries with code and name
        """
        print("[TRANSLATION] Fetching supported languages...")
        
        try:
            result = self.client.get_languages()
            
            languages = []
            for lang in result:
                code = lang['language']
                name = Config.get_language_name(code)
                languages.append({
                    'code': code,
                    'name': name,
                    'is_kmrl_primary': code in ['en', 'ml']
                })
            
            # Sort to put KMRL primary languages first
            languages.sort(key=lambda x: (not x['is_kmrl_primary'], x['name']))
            
            print(f"[TRANSLATION] ✅ Retrieved {len(languages)} supported languages")
            print("[TRANSLATION] KMRL primary languages: English, Malayalam")
            
            return languages
            
        except Exception as e:
            error_msg = f"Failed to get supported languages: {str(e)}"
            print(f"[TRANSLATION] ❌ {error_msg}")
            # Return at least the KMRL primary languages
            return [
                {'code': 'en', 'name': 'English', 'is_kmrl_primary': True},
                {'code': 'ml', 'name': 'Malayalam', 'is_kmrl_primary': True}
            ]
    
    def batch_translate(self, 
                       texts: List[str], 
                       target_language: str = 'en',
                       source_language: Optional[str] = None) -> List[TranslationResult]:
        """
        Batch translate multiple texts - Useful for KMRL document processing
        
        Args:
            texts: List of texts to translate
            target_language: Target language code
            source_language: Source language code (auto-detect if None)
            
        Returns:
            List of TranslationResult objects
        """
        print(f"[TRANSLATION] Starting batch translation for {len(texts)} texts to {target_language}")
        
        results = []
        for i, text in enumerate(texts):
            print(f"[TRANSLATION] Processing batch item {i+1}/{len(texts)}")
            result = self.translate_text(text, target_language, source_language)
            results.append(result)
        
        successful = sum(1 for r in results if not r.error)
        print(f"[TRANSLATION] ✅ Batch translation completed: {successful}/{len(texts)} successful")
        
        return results