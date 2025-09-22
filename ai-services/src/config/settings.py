# AI Services Configuration for DataTrack-KMRL
# Google Cloud Vision & Translation API Settings

import os
from typing import Dict, Any
from google.oauth2 import service_account
from google.cloud import vision, translate_v2 as translate

class Config:
    """Configuration management for Google Cloud services - DataTrack KMRL"""
    
    # Google Cloud credentials (embedded - no external files needed)
    GOOGLE_CREDENTIALS = {
        "type": "service_account",
        "project_id": "aiagent-465805",
        "private_key_id": "e4cfeb0fa6c442cd662f6b3b589e441b163610fb",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCZXRLf71w4SPeL\nXgXurYBy3PpMA2MQKU/PjczY/dSQKHUlkg9tuaHm5EyZdKlKSAo0qqATX9Qob7s/\nlfa3NBYSSgMfyzbvEpElPuXU5uyOX0mHCN5ZKE6qMfO+z5wK/GmreR84gkSXtgnE\nTVaz5xJI8QujdsFUL4bw9LgW1ZL/8voemPk0YbBSaqA9OkS3NW4dDJfhmdyv5Q9d\nTvVfdZDpnkt9i69Yn2R9K5/ctcYiWMNDnoWfFiqyN7veMjRh80xUfVjFyTTy4aEq\nPFVApP76v8QkA2NEgoE8KkuU5gwWiAtKTjtDOGJoiVkmPL9bZ10mOG51hftdeV0W\nSyY6LgCfAgMBAAECggEAISytdwxffftmtNqHXPxiAzbC2+uFo8rT7VlGnQ+3SeG+\niXyBYuJbX8c1vKIsNpnDv2XDT72UdpTIw/XsEvAs8BLbfyalwOxawlxLOhUjyZ5a\nGOA1vMKH1bANglKFdijosMN4GfCv5sNldHWoUi0jWuztcBQxuMS5I2lEYwgbDstK\nKtpke0X1FfO+yVPXVHWIdOww6J4z7m3NZykjZQQMAr81EmHg7b2Gl6s/X+67j1EB\n6gexMviHK0BOsaWCIA8SbUuCi4Ls2z1onKL054jJJTHcrLVjWa/h+a3jHDb2GRV+\nv2lAKpRgVgxXyobvb4zOsa6SXu9oVJq60NXDzBn5cQKBgQDR51/0+Q5HEhw1eMTr\n1m5YbTUHaaWegoJwMvpejm9PA9nkCBaWVZhE+f567m+Iz1eQGYCHkobAE4aNGV9D\nxL0eGG56RcwOjBW3qxSTgb8OXxVlP9v+S5MDgUARWKhGD0C09PLLf9U+Zx3heIzL\nIl2vwUc2LUw4YULg4rS2nLdoEQKBgQC7Cw04PrZ67DHoeiydkxE7i+Bzsk6BUuM5\npxVwacvwPiOuhAEKwLp/K+L4UvkhvVs7r+83xxiHXP9SJTknESQKorOB3uusFRQ8\nvlbVW14oeuPXwKQ/KqCHhDg3CYYis5iQvm/gfBNDKoRF6/4XhH0uZrdXxCcs1Q/X\npXXUbTUNrwKBgDZRGFytIkuz3QbdRJ/+sjlBsUpExW3aOeTM3Eshsp4Q0g6XJTkr\n1yZqRrcLAmO1u+P3JXJvsVz88IGMwkEoJQQnsFcFvsM47tnDdKSjG4ydgEzeFJCe\nf+GVTb3vYkQW6FirVjTg1I68YlgZON3L+9BiRIo5eJLSYFsPb1IeBbvxAoGAODrM\nUJpZ1X5oSpFgFEcAKTyVz3JNM4etk8ltIoxLqP+lTnOUtJzX9B9HbovTJZd9c+Yi\nLkyGTTth7loOYnY+tYvQFzzi8KqtmM1H4YBEQDshf90EA5FXDSZsl+8fChOfy/PU\nQlJKoCiJ91NI4d0MnQR4HcR0Wn/68UNmtuPVzTUCgYBAP1rsqYAJoEWlUN5iVLqk\nG8Vo6JEBOOcl3U5rPlyhp5rcrhdEWm1HorEB93BcFiGK17CRsx59NSP07rAxWJJ0\nGExK+USbSiSQtI+nuUeEPsfyA0ZUwXtQbO5cNubJ/5Lk6VcrJmaHHPQu65+zjwmZ\nOl/A2yu0l+0ulxLsYl40OQ==\n-----END PRIVATE KEY-----\n",
        "client_email": "datatrack-vision-service@aiagent-465805.iam.gserviceaccount.com",
        "client_id": "104353677060149455977",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/datatrack-vision-service%40aiagent-465805.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    
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
        """Get Google Cloud credentials from embedded config"""
        print("[CONFIG] Loading Google Cloud credentials for DataTrack-KMRL...")
        return service_account.Credentials.from_service_account_info(cls.GOOGLE_CREDENTIALS)
    
    @classmethod
    def get_vision_client(cls) -> vision.ImageAnnotatorClient:
        """Get configured Vision API client for OCR processing"""
        credentials = cls.get_credentials()
        print("[CONFIG] Initializing Google Vision client...")
        return vision.ImageAnnotatorClient(credentials=credentials)
    
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
