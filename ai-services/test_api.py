"""
Test script to verify the classification API is working correctly
"""
import sys
import os
import json
import requests

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Sample test texts
test_texts = {
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
    """
}

def test_classification_api():
    """Test the classification API endpoint"""
    api_url = "http://localhost:8001/api/classification/text"
    
    for doc_type, text in test_texts.items():
        print(f"\n--- TESTING {doc_type.upper()} DOCUMENT ---")
        
        # Prepare the request
        request_data = {
            "text": text,
            "min_confidence": 0.0
        }
        
        try:
            # Send the request
            response = requests.post(api_url, json=request_data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse the response
            result = response.json()
            
            # Print the result
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(result, indent=2)}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_classification_api()