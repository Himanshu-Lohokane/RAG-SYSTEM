"""
Document classification service for KMRL document management system

This module provides document classification functionality using
Google Cloud Natural Language API, which offers pre-trained models
for document classification without requiring custom training.
"""

from typing import Dict, List, Optional, Tuple
import time
import logging
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config

# Import Google Cloud Natural Language API - with proper error handling for import
try:
    from google.cloud import language_v1
    HAS_GOOGLE_LANGUAGE = True
    logging.info("Successfully imported Google Cloud Language API")
except ImportError:
    HAS_GOOGLE_LANGUAGE = False
    logging.warning("Google Cloud Language API not available. Using keyword-based classification only.")

# Document categories for KMRL
DOCUMENT_CATEGORIES = [
    "Engineering Drawings",
    "Maintenance job cards",
    "Incident reports", 
    "Vendor invoices",
    "Purchase-order correspondence",
    "Regulatory directives",
    "Environmental-impact studies",
    "Safety circulars",
    "HR policies",
    "Legal opinions",
    "Board meeting minutes"
]

# This mapping helps translate Google's content categories to KMRL categories
# The keys are partial matches of Google categories, and values are KMRL categories
GOOGLE_TO_KMRL_CATEGORY_MAPPING = {
    # Engineering
    "/Science/Engineering": "Engineering Drawings",
    "/Business/Manufacturing": "Engineering Drawings",
    "/Science/Technology": "Engineering Drawings",
    "/Science/Engineering & Technology": "Engineering Drawings",
    "/Arts & Entertainment/Visual Art & Design": "Engineering Drawings",
    
    # Maintenance
    "/Business/Industrial Goods & Services": "Maintenance job cards",
    "/Autos & Vehicles/Vehicle Repair & Maintenance": "Maintenance job cards",
    "/Business/Business Operations/Management": "Maintenance job cards",
    
    # Incident reports
    "/Law & Government/Public Safety": "Incident reports",
    "/Health/Health & Safety": "Incident reports",
    "/Law & Government/Legal/Legal Services": "Incident reports",
    
    # Vendor invoices
    "/Finance/Accounting & Auditing": "Vendor invoices",
    "/Finance/Financial Documents": "Vendor invoices",
    "/Business/Business Operations/Business Plans & Presentations": "Vendor invoices",
    
    # Purchase orders
    "/Business/Business Operations/Supply Chain & Logistics": "Purchase-order correspondence",
    "/Finance/Investing/Commodities & Futures Trading": "Purchase-order correspondence",
    "/Finance/Financial Planning": "Purchase-order correspondence",
    
    # Regulatory
    "/Law & Government": "Regulatory directives",
    "/Law & Government/Government": "Regulatory directives",
    "/Law & Government/Legal": "Regulatory directives",
    
    # Environmental
    "/Science/Ecology & Environment": "Environmental-impact studies",
    "/Science/Earth Sciences": "Environmental-impact studies",
    "/Science/Weather": "Environmental-impact studies",
    
    # Safety
    "/Health/Health & Safety": "Safety circulars",
    "/Law & Government/Public Safety": "Safety circulars",
    "/Health/Medical Facilities & Services": "Safety circulars",
    "/Health/Public Health/Occupational Health & Safety": "Safety circulars",
    
    # HR
    "/Business/Business Operations/Human Resources": "HR policies",
    "/Jobs & Education": "HR policies",
    "/People & Society": "HR policies",
    "/Business & Industrial/Business Operations/Human Resources": "HR policies",
    "/Business & Industrial/Business Operations": "HR policies",  # Keep this but improve the matching logic
    
    # Financial
    "/Finance": "Vendor invoices",
    "/News/Business News": "Vendor invoices",
    "/Business & Industrial/Accounting & Finance": "Vendor invoices",
    "/Business & Industrial": "Vendor invoices",  # Keep as fallback but improve the matching logic
    
    # Legal
    "/Law & Government/Legal": "Legal opinions",
    "/Law & Government/Legal/Legal Services": "Legal opinions",
    "/Business/Business Operations/Business Plans & Presentations": "Legal opinions",
    
    # Board meetings
    "/Business/Business Operations/Business Plans & Presentations": "Board meeting minutes",
    "/Business/Business Operations/Management": "Board meeting minutes",
    "/Finance/Investing/Stocks & Bonds": "Board meeting minutes"
}

# Fallback to keyword matching for edge cases where Google's classification might not be specific enough
CATEGORY_KEYWORDS = {
    "Engineering Drawings": [
        "drawing", "blueprint", "schematic", "technical drawing", "dimensions", 
        "CAD", "isometric", "mechanical drawing", "electrical diagram"
    ],
    "Maintenance job cards": [
        "job card", "work order", "service report", "maintenance task", "inspection report"
    ],
    "Incident reports": [
        "incident", "accident", "report", "safety incident", "investigation", "root cause"
    ],
    "Vendor invoices": [
        "invoice", "bill", "payment", "vendor", "supplier", "invoice number", "billing"
    ],
    "Purchase-order correspondence": [
        "purchase order", "PO", "order confirmation", "requisition", "procurement"
    ],
    "Regulatory directives": [
        "regulation", "compliance", "directive", "regulatory requirement", "statutory"
    ],
    "Environmental-impact studies": [
        "environmental impact", "ecological", "assessment", "EIA", "sustainability"
    ],
    "Safety circulars": [
        "safety", "circular", "safety notice", "alert", "safety bulletin", "warning"
    ],
    "HR policies": [
        "HR", "human resources", "policy", "employee", "personnel", "employment"
    ],
    "Legal opinions": [
        "legal opinion", "legal advice", "counsel", "attorney", "legal analysis"
    ],
    "Board meeting minutes": [
        "board meeting", "minutes", "resolution", "board of directors", "meeting agenda"
    ]
}


class ClassificationService:
    """Document classification service for KMRL using Google Cloud Natural Language API"""
    
    def __init__(self):
        """Initialize the classification service with Google Cloud Natural Language client"""
        self.language_client = None
        self.use_google_api = False
        self.current_text = ""  # Store the current text being processed
        
        # Attempt to initialize the Language API client with existing credentials
        # from the same configuration used by other services
        if HAS_GOOGLE_LANGUAGE:
            try:
                # Use the same credentials and project settings as the rest of the application
                credentials = Config.get_credentials()
                self.language_client = language_v1.LanguageServiceClient(credentials=credentials)
                self.use_google_api = True
                print("[CLASS] Google Cloud Natural Language API client initialized successfully")
                print(f"[CLASS] Using project: {Config.PROJECT_ID}")
            except Exception as e:
                self.use_google_api = False
                print(f"[CLASS] ❌ Failed to initialize Google Cloud Natural Language API: {e}")
                print("[CLASS] Falling back to keyword-based classification")
        else:
            print("[CLASS] Google Cloud Language API not available. Using keyword-based classification only.")
    
    def _find_best_kmrl_category(self, google_categories: List[Dict]) -> Tuple[str, float]:
        """
        Map Google's content categories to KMRL document categories
        
        Args:
            google_categories: List of categories returned by Google Natural Language API
            
        Returns:
            Tuple of (best_matching_category, confidence)
        """
        if not google_categories:
            return "Unknown", 0.0
            
        # Dictionary to track scores for KMRL categories
        kmrl_scores = {category: 0.0 for category in DOCUMENT_CATEGORIES}
        
        # Special handling for HR vs Financial documents
        hr_keywords = ["human resources", "employee", "leave", "policy", "staff", "personnel"]
        financial_keywords = ["financial", "revenue", "expense", "budget", "invoice", "payment", "fiscal"]
        
        # Process each Google category
        for category_data in google_categories:
            google_category = category_data.name
            confidence = category_data.confidence
            
            # Check for special cases based on category
            if google_category == "/Business & Industrial/Business Operations":
                # This category could be HR or Financial - check document content
                is_hr = any(kw in self.current_text.lower() for kw in hr_keywords)
                is_financial = any(kw in self.current_text.lower() for kw in financial_keywords)
                
                if is_hr and not is_financial:
                    kmrl_scores["HR policies"] += confidence * 1.2  # Boost HR confidence
                    continue
                elif is_financial and not is_hr:
                    kmrl_scores["Vendor invoices"] += confidence * 1.2  # Boost Financial confidence
                    continue
            
            # Find matching KMRL categories from the mapping
            for google_pattern, kmrl_category in GOOGLE_TO_KMRL_CATEGORY_MAPPING.items():
                if google_pattern in google_category:
                    # Add the confidence score to the matching KMRL category
                    # Give higher weight to more specific (longer) patterns
                    specificity_boost = len(google_pattern) / 20  # Longer patterns get higher boost
                    kmrl_scores[kmrl_category] += confidence * (1 + specificity_boost)
        
        # Find the KMRL category with the highest score
        best_category = max(kmrl_scores.items(), key=lambda x: x[1])
        
        if best_category[1] > 0:
            return best_category[0], best_category[1]
        else:
            return "Unknown", 0.0
    
    def _classify_with_google_api(self, text: str) -> Dict:
        """
        Classify a document using Google Cloud Natural Language API
        
        Args:
            text: Document text content
            
        Returns:
            Classification results dictionary
        """
        if not HAS_GOOGLE_LANGUAGE:
            logging.error("Google Cloud Language API not available")
            return None
            
        try:
            # Create a Document object
            document = language_v1.Document(
                content=text,
                type_=language_v1.Document.Type.PLAIN_TEXT
            )
            
            # Use content classification from Natural Language API
            try:
                response = self.language_client.classify_text(document=document)
                logging.info("Google Cloud Natural Language API classification successful!")
            except Exception as e:
                logging.error(f"Google API classification failed: {e}")
                # If this is a SERVICE_DISABLED error, provide more specific guidance
                if "SERVICE_DISABLED" in str(e) and "data-axle-firebase" in str(e):
                    logging.error("Please enable the Natural Language API in the Google Cloud Console for project 'data-axle-firebase'")
                    logging.error("Visit: https://console.cloud.google.com/apis/library/language.googleapis.com?project=data-axle-firebase")
                return None
        except Exception as e:
            logging.error(f"Error preparing document for classification: {e}")
            return None
            
        # Process Google's classification results
        google_categories = []
        
        for category in response.categories:
            google_categories.append({
                "name": category.name,
                "confidence": category.confidence
            })
            
        # Map Google's categories to KMRL categories
        best_kmrl_category, confidence = self._find_best_kmrl_category(response.categories)
        
        # Prepare all categories with confidence scores
        all_categories = []
        
        # Track which KMRL categories have been matched
        matched_kmrl_categories = set()
        
        for category in response.categories:
            # Find matching KMRL categories
            matched_categories = []
            for google_pattern, kmrl_category in GOOGLE_TO_KMRL_CATEGORY_MAPPING.items():
                if google_pattern in category.name:
                    matched_categories.append(kmrl_category)
                    matched_kmrl_categories.add(kmrl_category)
            
            # Add each matched category to results
            for kmrl_category in matched_categories:
                all_categories.append({
                    "category": kmrl_category,
                    "google_category": category.name,
                    "confidence": category.confidence
                })
        
        # Sort by confidence
        all_categories.sort(key=lambda x: x["confidence"], reverse=True)
        
        return {
            "category": best_kmrl_category,
            "confidence": confidence,
            "all_categories": all_categories,
            "google_categories": google_categories,
            "method": "google-cloud-natural-language"
        }

    def _classify_with_keywords(self, text: str) -> Dict:
        """
        Fallback classification method using keyword matching
        
        Args:
            text: Document text content
            
        Returns:
            Classification results dictionary
        """
        # Calculate scores for each category based on keyword matches
        scores = {}
        text_lower = text.lower()
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            # Initialize score for this category
            score = 0
            matches = []
            
            # Check for keyword matches
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in text_lower:
                    # Count occurrences of the keyword
                    import re
                    match_count = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', text_lower))
                    if match_count > 0:
                        keyword_score = len(keyword) * match_count
                        score += keyword_score
                        matches.append(f"{keyword} ({match_count})")
            
            # Only include categories with matches
            if score > 0:
                scores[category] = {
                    "score": score,
                    "matches": matches
                }
        
        # Sort categories by score
        sorted_categories = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
        
        # Calculate total score for confidence calculation
        total_score = sum(item[1]["score"] for item in sorted_categories)
        
        # Prepare results
        results = []
        for category, data in sorted_categories:
            confidence = data["score"] / total_score if total_score > 0 else 0
            results.append({
                "category": category,
                "confidence": confidence,
                "matched_keywords": data["matches"]
            })
        
        return {
            "category": sorted_categories[0][0] if sorted_categories else "Unknown",
            "confidence": sorted_categories[0][1]["score"] / total_score if sorted_categories and total_score > 0 else 0.0,
            "all_categories": results,
            "method": "keyword-fallback"
        }
    
    def classify_document(self, text: str) -> Dict:
        """
        Classify a document based on its text content using Google Cloud Natural Language API
        with fallback to keyword-based classification if API fails
        
        Args:
            text: Extracted text from the document
            
        Returns:
            Dictionary with classification results
        """
        start_time = time.time()
        
        if not text:
            return {
                "category": "Unknown",
                "confidence": 0.0,
                "all_categories": [],
                "processing_time_seconds": time.time() - start_time,
                "method": "none"
            }
        
        # Store the current text for use in classification logic
        self.current_text = text
        
        # Trim text if too long (Google API has a limit)
        # The limit is 100KB, but we'll use a lower threshold to be safe
        if len(text) > 90000:
            text = text[:90000]
        
        # Try Google Cloud Natural Language API first
        if self.use_google_api and len(text.strip()) > 20:  # Only use API if there's substantial text
            try:
                google_results = self._classify_with_google_api(text)
                if google_results:
                    google_results["processing_time_seconds"] = time.time() - start_time
                    return google_results
            except Exception as e:
                logging.error(f"Error using Google Cloud Natural Language API: {e}")
                # Fall back to keyword-based classification
        
        # Fallback to keyword-based classification
        keyword_results = self._classify_with_keywords(text)
        keyword_results["processing_time_seconds"] = time.time() - start_time
        return keyword_results
