# AI Services Configuration for DataTrack-KMRL
# Google Cloud Vision & Translation API Settings

import os
import json
from typing import Dict, Any
from google.oauth2 import service_account
from google.cloud import vision, translate_v2 as translate

class Config:
    """Configuration management for Google Cloud services - DataTrack KMRL"""
    
    # Google Cloud credentials will be loaded from environment variable only
    
    PROJECT_ID = "aiagent-465805"
    
    # KMRL Specific Language Mappings (English + Malayalam focus)
    LANGUAGE_NAMES = {
        # KMRL Primary Languages
        'en': 'English',
        'ml': 'Malayalam',
        
        # Indian Regional Languages (for potential expansion)
        'hi': 'Hindi', 'ta': 'Tamil', 'te': 'Telugu', 'kn': 'Kannada',
        'gu': 'Gujarati', 'bn': 'Bengali', 'pa': 'Punjabi', 'mr': 'Marathi',
        'or': 'Odia', 'as': 'Assamese', 'ur': 'Urdu', 'sa': 'Sanskrit',
        
        # International Languages
        'es': 'Spanish', 'fr': 'French', 'de': 'German', 'zh': 'Chinese',
        'ja': 'Japanese', 'ko': 'Korean', 'ar': 'Arabic', 'ru': 'Russian',
        'it': 'Italian', 'pt': 'Portuguese'
    }
    
    # KMRL Document Categories for Future Classification
    KMRL_DOCUMENT_CATEGORIES = {
        'engineering': 'Engineering & Technical',
        'safety': 'Safety & Security',
        'financial': 'Financial & Procurement', 
        'hr': 'Human Resources',
        'operations': 'Operations & Maintenance',
        'regulatory': 'Regulatory & Compliance',
        'environment': 'Environmental Impact',
        'legal': 'Legal & Contracts',
        'training': 'Training & Development',
        'general': 'General Administration'
    }
    
    @classmethod
    def get_credentials(cls) -> service_account.Credentials:
        """Get Google Cloud credentials from environment variable"""
        print("[CONFIG] Loading Google Cloud credentials for DataTrack-KMRL...")
        
        # Load from environment variable (required for security)
        credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        if not credentials_json:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable is required")
        
        try:
            print("[CONFIG] Using credentials from environment variable")
            credentials_dict = json.loads(credentials_json)
            return service_account.Credentials.from_service_account_info(credentials_dict)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse credentials from environment: {e}")
    
    @classmethod
    def get_vision_client(cls) -> vision.ImageAnnotatorClient:
        """Get configured Vision API client for OCR processing"""
        try:
            credentials = cls.get_credentials()
            print("[CONFIG] Initializing Google Vision client...")
            print(f"[CONFIG] Service account email: {credentials.service_account_email}")
            print(f"[CONFIG] Project ID: {cls.PROJECT_ID}")
            client = vision.ImageAnnotatorClient(credentials=credentials)
            print("[CONFIG] ✅ Vision client created successfully")
            return client
        except Exception as e:
            print(f"[CONFIG] ❌ Failed to create Vision client: {e}")
            raise
    
    @classmethod
    def get_translate_client(cls) -> translate.Client:
        """Get configured Translation API client"""
        credentials = cls.get_credentials()
        print("[CONFIG] Initializing Google Translation client...")
        return translate.Client(credentials=credentials)
    
    @classmethod
    def get_language_name(cls, language_code: str) -> str:
        """Convert language code to full name"""
        return cls.LANGUAGE_NAMES.get(language_code, language_code.upper())
    
    @classmethod
    def get_kmrl_category_name(cls, category_code: str) -> str:
        """Get KMRL document category full name"""
        return cls.KMRL_DOCUMENT_CATEGORIES.get(category_code, 'Unknown Category')
