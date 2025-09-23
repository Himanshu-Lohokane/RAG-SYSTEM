"""
Document classification service for KMRL document management system

This module provides document classification functionality using
the Google Cloud Vision API that's already being used in the project.
"""

from typing import Dict, List, Optional
import time
import re

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

# Keywords associated with each category
CATEGORY_KEYWORDS = {
    "Engineering Drawings": [
        "drawing", "blueprint", "schematic", "technical drawing", "dimensions", 
        "scale", "elevation", "floor plan", "cross section", "isometric", "CAD", 
        "layout", "design drawing", "mechanical drawing", "electrical diagram"
    ],
    "Maintenance job cards": [
        "job card", "maintenance record", "work order", "service report", "repair", 
        "maintenance task", "equipment service", "inspection report", "fault report", 
        "maintenance schedule", "job completion", "technician", "service date"
    ],
    "Incident reports": [
        "incident", "accident", "report", "safety incident", "occurrence", "event report",
        "investigation", "root cause", "corrective action", "preventive action", 
        "injury", "property damage", "witness statement", "incident location"
    ],
    "Vendor invoices": [
        "invoice", "bill", "payment", "vendor", "supplier", "amount", "due date",
        "invoice number", "billing", "purchase", "item", "quantity", "unit price",
        "tax amount", "total amount", "payment terms", "account number"
    ],
    "Purchase-order correspondence": [
        "purchase order", "PO", "order confirmation", "requisition", "procurement",
        "order acknowledgment", "delivery schedule", "order details", "change order",
        "order number", "buyer", "supplier", "delivery date", "order quantity"
    ],
    "Regulatory directives": [
        "regulation", "compliance", "directive", "regulatory requirement", "authority",
        "compliance report", "regulatory body", "statutory", "legal requirement",
        "regulatory framework", "compliance deadline", "regulatory notification"
    ],
    "Environmental-impact studies": [
        "environmental impact", "ecological", "assessment", "EIA", "sustainability",
        "environmental study", "environmental factor", "mitigation measure", "biodiversity",
        "pollution", "environmental monitoring", "ecosystem", "environmental compliance"
    ],
    "Safety circulars": [
        "safety", "circular", "safety notice", "alert", "safety bulletin", "warning",
        "safety procedure", "precaution", "safety requirement", "safety protocol",
        "hazard notification", "safety guideline", "safety compliance"
    ],
    "HR policies": [
        "HR", "human resources", "policy", "employee", "personnel", "employment",
        "workplace policy", "staff", "benefit", "compensation", "leave policy",
        "code of conduct", "HR guideline", "recruitment", "performance evaluation"
    ],
    "Legal opinions": [
        "legal opinion", "legal advice", "counsel", "attorney", "legal analysis",
        "legal assessment", "legal recommendation", "legal conclusion", "legal review",
        "legal position", "legal interpretation", "law firm", "legal consultation"
    ],
    "Board meeting minutes": [
        "board meeting", "minutes", "resolution", "board of directors", "chairperson",
        "meeting agenda", "board decision", "board approval", "meeting date",
        "board member", "quorum", "motion", "voting", "board resolution"
    ]
}

class ClassificationService:
    """Document classification service for KMRL"""
    
    def __init__(self):
        """Initialize the classification service"""
        pass
    
    def classify_document(self, text: str) -> Dict:
        """
        Classify a document based on its text content
        
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
                "processing_time_seconds": time.time() - start_time
            }
        
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
                    # Add score based on keyword length and frequency
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
        
        # Return classification results
        return {
            "category": sorted_categories[0][0] if sorted_categories else "Unknown",
            "confidence": sorted_categories[0][1]["score"] / total_score if sorted_categories and total_score > 0 else 0.0,
            "all_categories": results,
            "processing_time_seconds": time.time() - start_time
        }
