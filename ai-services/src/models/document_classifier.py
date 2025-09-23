"""
Document Classifier for KMRL Document Management System

This module provides classification functionality to categorize KMRL documents into
predefined categories using Google Cloud Vision API.

Categories:
- Engineering Drawings
- Maintenance job cards
- Incident reports
- Vendor invoices
- Purchase-order correspondence
- Regulatory directives
- Environmental-impact studies
- Safety circulars
- HR policies
- Legal opinions
- Board meeting minutes
"""

from typing import Dict, List, Optional, Tuple
import os
import json
from google.cloud import vision
from google.cloud.vision_v1 import types
import io
import re

# Document categories
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

# Keywords and patterns associated with each category
CATEGORY_KEYWORDS = {
    "Engineering Drawings": [
        "drawing", "blueprint", "schematic", "technical drawing", "engineering spec", 
        "dimensions", "scale", "elevation", "floor plan", "cross section", "isometric",
        "CAD", "AutoCAD", "layout", "design drawing", "mechanical drawing", "electrical diagram",
        "assembly drawing", "fabrication", "engineering detail", "drawing number"
    ],
    "Maintenance job cards": [
        "job card", "maintenance record", "work order", "service report", "repair", 
        "maintenance task", "preventive maintenance", "equipment service", "inspection report",
        "fault report", "maintenance schedule", "job completion", "technician", "service date",
        "maintenance personnel", "equipment id", "service hours", "parts replaced"
    ],
    "Incident reports": [
        "incident", "accident", "report", "safety incident", "occurrence", "event report",
        "investigation", "root cause", "corrective action", "preventive action", "incident date",
        "injury", "property damage", "witness statement", "incident location", "severity",
        "hazard", "incident description", "reporting person"
    ],
    "Vendor invoices": [
        "invoice", "bill", "payment", "vendor", "supplier", "amount", "due date",
        "invoice number", "billing", "purchase", "item", "quantity", "unit price",
        "tax amount", "total amount", "payment terms", "account number", "billing address",
        "invoice date", "payment due", "subtotal"
    ],
    "Purchase-order correspondence": [
        "purchase order", "PO", "order confirmation", "requisition", "procurement",
        "order acknowledgment", "delivery schedule", "order details", "change order",
        "order number", "buyer", "supplier", "delivery date", "order quantity",
        "item description", "shipping terms", "order amendment", "price quote"
    ],
    "Regulatory directives": [
        "regulation", "compliance", "directive", "regulatory requirement", "authority",
        "compliance report", "regulatory body", "statutory", "legal requirement",
        "regulatory framework", "compliance deadline", "regulatory notification",
        "regulator", "regulatory standard", "enforcement", "compliance measure",
        "regulatory update", "legal obligation"
    ],
    "Environmental-impact studies": [
        "environmental impact", "ecological", "assessment", "EIA", "sustainability",
        "environmental study", "environmental factor", "mitigation measure", "biodiversity",
        "pollution", "environmental monitoring", "ecosystem", "environmental compliance",
        "environmental management", "carbon footprint", "environmental risk", "habitat"
    ],
    "Safety circulars": [
        "safety", "circular", "safety notice", "alert", "safety bulletin", "warning",
        "safety procedure", "precaution", "safety requirement", "safety protocol",
        "hazard notification", "safety guideline", "safety compliance", "safety instruction",
        "protective measure", "safety equipment", "safety training", "emergency procedure"
    ],
    "HR policies": [
        "HR", "human resources", "policy", "employee", "personnel", "employment",
        "workplace policy", "staff", "benefit", "compensation", "leave policy",
        "code of conduct", "HR guideline", "recruitment", "performance evaluation",
        "disciplinary procedure", "grievance", "employee handbook", "organization policy"
    ],
    "Legal opinions": [
        "legal opinion", "legal advice", "counsel", "attorney", "legal analysis",
        "legal assessment", "legal recommendation", "legal conclusion", "legal review",
        "legal position", "legal interpretation", "law firm", "legal consultation",
        "legal expert", "judicial", "statute", "legal precedent", "legal matter", "jurisdiction"
    ],
    "Board meeting minutes": [
        "board meeting", "minutes", "resolution", "board of directors", "chairperson",
        "meeting agenda", "board decision", "board approval", "meeting date",
        "board member", "quorum", "motion", "voting", "board resolution",
        "corporate governance", "executive session", "board secretary", "director", "trustee"
    ]
}

class DocumentClassifier:
    """Document classifier for KMRL documents"""
    
    def __init__(self):
        """Initialize the document classifier"""
        # Set up Google Cloud Vision client
        self.client = vision.ImageAnnotatorClient()
    
    def extract_text_from_image(self, image_content: bytes) -> str:
        """
        Extract text from an image using Google Cloud Vision API
        
        Args:
            image_content: Binary content of the image
            
        Returns:
            Extracted text from the image
        """
        image = types.Image(content=image_content)
        response = self.client.text_detection(image=image)
        texts = response.text_annotations
        
        if not texts:
            return ""
            
        return texts[0].description

    def classify_document(self, image_content: bytes) -> Dict:
        """
        Classify a document based on its content
        
        Args:
            image_content: Binary content of the image
            
        Returns:
            Dictionary with classification results
        """
        # Extract text from image
        start_time = __import__('time').time()
        extracted_text = self.extract_text_from_image(image_content)
        
        if not extracted_text:
            return {
                "category": "Unknown",
                "confidence": 0.0,
                "extracted_text": "",
                "processing_time_seconds": __import__('time').time() - start_time
            }
        
        # Calculate scores for each category based on keyword matches
        scores = {}
        text_lower = extracted_text.lower()
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            # Initialize score for this category
            score = 0
            matches = []
            
            # Check for keyword matches
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in text_lower:
                    # Add score based on keyword length (longer keywords are more specific)
                    match_count = text_lower.count(keyword_lower)
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
        
        # Return classification results
        return {
            "category": sorted_categories[0][0] if sorted_categories else "Unknown",
            "confidence": sorted_categories[0][1]["score"] / total_score if sorted_categories and total_score > 0 else 0.0,
            "all_categories": results,
            "extracted_text": extracted_text,
            "processing_time_seconds": __import__('time').time() - start_time
        }
