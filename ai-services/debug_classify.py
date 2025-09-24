"""
Debug script for investigating classification issues with HR and financial documents
"""
import sys
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config.settings import Config
from src.services.classification_service import ClassificationService

# Test documents
test_documents = {
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
    HUMAN RESOURCES POLICY DOCUMENT
    Policy Number: HR-POL-2023-018
    Effective Date: December 1, 2023
    
    EMPLOYEE LEAVE POLICY
    
    1. PURPOSE
    This policy establishes guidelines for requesting and approving employee leave and vacation time.
    
    2. SCOPE
    This policy applies to all permanent employees of Kochi Metro Rail Limited across all departments and positions.
    
    3. POLICY DETAILS
    3.1 Annual Leave Entitlement
    - Junior staff: 20 days per year
    - Middle management: 25 days per year
    - Senior management: 30 days per year
    
    3.2 Sick Leave Entitlement
    - All employees are entitled to 15 days of paid sick leave per year
    - Medical certificate required for sick leave exceeding 3 consecutive days
    
    3.3 Application Process
    All leave applications must be submitted through the HRMS system at least 7 days in advance for approval by the department head.
    """,
    
    "financial": """
    FINANCIAL REPORT - QUARTERLY STATEMENT
    Q2 2023 FISCAL REVIEW
    KOCHI METRO RAIL LIMITED
    
    EXECUTIVE SUMMARY
    This quarterly financial statement presents the revenue, expenses, and profit margins for Kochi Metro Rail Limited operations from April to June 2023. Total revenue increased by 12% compared to the previous quarter, with fare collection showing significant growth of 15.3%.
    
    FINANCIAL HIGHLIGHTS
    • Total Revenue: ₹157.8 crores (12% increase from Q1)
    • Operating Expenses: ₹112.3 crores (5% increase from Q1)
    • Net Profit: ₹45.5 crores (31% increase from Q1)
    • Debt Service Coverage Ratio: 1.42 (improved from 1.28 in Q1)
    
    REVENUE BREAKDOWN
    1. Fare Collection: ₹135.2 crores (85.7% of total)
    2. Commercial Space Rental: ₹15.6 crores (9.9% of total)
    3. Advertising: ₹7.0 crores (4.4% of total)
    
    This report has been prepared in accordance with Indian Accounting Standards (Ind AS) and approved by the Finance Department.
    """
}

def debug_classification_for_document(service, doc_type, text):
    """Run classification with detailed logging for a document"""
    logging.info(f"\n\n--- TESTING CLASSIFICATION FOR {doc_type.upper()} DOCUMENT ---")
    
    # Try Google API directly
    logging.info(f"Text length: {len(text)} characters")
    
    try:
        if not service.use_google_api:
            logging.warning("Google API not available or not configured!")
        
        # Enable more logging in Google API method
        logging.info("Attempting direct Google Cloud Natural Language API classification...")
        
        # Create a document object
        from google.cloud import language_v1
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT
        )
        
        # Call the API directly
        response = service.language_client.classify_text(document=document)
        
        # Log the raw response
        logging.info(f"Raw API response: {response}")
        
        # Log each category
        for category in response.categories:
            logging.info(f"Category: {category.name}, Confidence: {category.confidence}")
            
        # Now call the service method and show results
        result = service.classify_document(text)
        logging.info(f"Final classification: {json.dumps(result, indent=2)}")
        return result
        
    except Exception as e:
        logging.error(f"Error during classification: {e}")
        return None

def main():
    """Main function to test classification"""
    logging.info("Creating classification service...")
    service = ClassificationService()
    
    # Test each document type
    for doc_type, text in test_documents.items():
        result = debug_classification_for_document(service, doc_type, text)

if __name__ == "__main__":
    main()