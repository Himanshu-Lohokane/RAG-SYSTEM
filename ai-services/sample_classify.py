"""
Sample script to demonstrate document classification using Google Cloud Natural Language API

This script shows how to use the new classification service that uses Google Cloud 
Natural Language API for document classification without requiring custom training.

Usage:
    python sample_classify.py [text_file.txt]
    
    If no file is provided, the script will use sample texts.
"""

import sys
import os
import time
import json

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config.settings import Config

try:
    from google.cloud import language_v1
    from google.api_core.client_options import ClientOptions
    HAS_GOOGLE_LANGUAGE = True
except ImportError:
    HAS_GOOGLE_LANGUAGE = False
    print("Google Cloud Language API not available. Please install with: pip install google-cloud-language==2.13.1")

def classify_text_with_natural_language_api(text_content):
    """
    Classifies text content using Google Cloud Natural Language API.
    
    Args:
        text_content: Text to be classified
    
    Returns:
        Dictionary with classification results
    """
    start_time = time.time()
    
    if not HAS_GOOGLE_LANGUAGE:
        return {
            "classification_successful": False,
            "error": "Google Cloud Language API not available. Please install with: pip install google-cloud-language==2.13.1",
            "processing_time_seconds": time.time() - start_time,
            "method": "none"
        }
    
    try:
        # Get credentials from Config
        credentials = Config.get_credentials()
        
        # Initialize the Natural Language client with the correct project from Config
        client_options = ClientOptions(quota_project_id=Config.PROJECT_ID)
        client = language_v1.LanguageServiceClient(credentials=credentials, client_options=client_options)
        
        print(f"Using project: {Config.PROJECT_ID}")
        
        # Prepare the document
        document = language_v1.Document(
            content=text_content,
            type_=language_v1.Document.Type.PLAIN_TEXT
        )
        
        # Analyze the document
        response = client.classify_text(document=document)
        
        # Process results
        categories = []
        for category in response.categories:
            categories.append({
                "name": category.name,
                "confidence": category.confidence
            })
        
        # Sort categories by confidence
        categories.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Return results
        result = {
            "classification_successful": True,
            "top_category": categories[0]["name"] if categories else "Unknown",
            "top_confidence": categories[0]["confidence"] if categories else 0.0,
            "all_categories": categories,
            "processing_time_seconds": time.time() - start_time,
            "method": "google-cloud-natural-language"
        }
        
        return result
    
    except Exception as e:
        return {
            "classification_successful": False,
            "error": str(e),
            "processing_time_seconds": time.time() - start_time,
            "method": "google-cloud-natural-language"
        }

def pretty_print_result(result):
    """
    Print the classification result in a human-readable format.
    
    Args:
        result: Classification result dictionary
    """
    print("\n" + "="*60)
    print("DOCUMENT CLASSIFICATION RESULTS")
    print("="*60)
    
    if result["classification_successful"]:
        print(f"Top Category: {result['top_category']}")
        print(f"Confidence: {result['top_confidence']:.4f}")
        print(f"Classification Method: {result['method']}")
        print(f"Processing Time: {result['processing_time_seconds']:.4f} seconds")
        
        print("\nAll Categories:")
        for i, category in enumerate(result["all_categories"], 1):
            print(f"  {i}. {category['name']} (Confidence: {category['confidence']:.4f})")
    else:
        print(f"Classification Failed: {result['error']}")
    
    print("="*60)

def main():
    print("\nDocument Classification using Google Cloud Natural Language API")
    print("-" * 60)
    print(f"NOTE: This script uses Google Cloud credentials from Config")
    print(f"      Project ID: {Config.PROJECT_ID}\n")
    
    # Sample texts for different document types
    sample_texts = {
        "engineering": """
        Technical Drawing: Front Elevation
        Scale: 1:100
        Drawing No.: ENG-2023-045
        
        This technical drawing shows the front elevation of the proposed station building
        including dimensions, structural elements, and architectural features.
        All measurements are in millimeters unless otherwise specified.
        
        The drawing includes the following details:
        - Foundation specifications
        - Steel column placements
        - Beam dimensions and specifications
        - External wall treatments
        - Window and door placements
        """,
        
        "safety": """
        SAFETY CIRCULAR
        REF: KMRL/SAFETY/2023/056
        Date: November 10, 2023
        
        SUBJECT: Updated Safety Protocols for Maintenance Staff
        
        All maintenance staff are hereby notified of the following updated safety protocols:
        
        1. Always wear appropriate PPE when working on electrical systems
        2. Ensure proper lockout/tagout procedures are followed for all maintenance activities
        3. Report all safety incidents immediately to shift supervisors
        4. Weekly safety briefings are now mandatory for all maintenance teams
        
        These measures are being implemented to ensure the highest safety standards across
        all KMRL facilities and operations.
        """,
        
        "hr": """
        HUMAN RESOURCES POLICY
        Policy Number: HR-POL-2023-018
        Effective Date: December 1, 2023
        
        EMPLOYEE LEAVE POLICY
        
        1. PURPOSE
        This policy establishes guidelines for requesting and approving employee leave.
        
        2. SCOPE
        This policy applies to all permanent employees of Kochi Metro Rail Limited.
        
        3. POLICY DETAILS
        3.1 Annual Leave Entitlement
        - Junior staff: 20 days per year
        - Middle management: 25 days per year
        - Senior management: 30 days per year
        
        3.2 Sick Leave Entitlement
        - All employees are entitled to 15 days of paid sick leave per year
        
        3.3 Application Process
        All leave applications must be submitted through the HRMS system at least 7 days in advance.
        """
    }
    
    # Determine which text to use
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        # Use text from file
        file_path = sys.argv[1]
        print(f"Reading text from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
        
        # Classify the text
        result = classify_text_with_natural_language_api(text_content)
        pretty_print_result(result)
    else:
        # Use sample texts
        print("No file provided. Using sample texts...")
        for doc_type, sample in sample_texts.items():
            print(f"\n\n--- CLASSIFYING SAMPLE: {doc_type.upper()} ---")
            result = classify_text_with_natural_language_api(sample)
            pretty_print_result(result)

if __name__ == "__main__":
    main()