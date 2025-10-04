"""
Test script for Google Cloud credentials configuration
"""
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config.settings import Config

def test_credentials():
    """Test that the Google Cloud credentials are working"""
    print(f"Project ID from config: {Config.PROJECT_ID}")
    
    # Try to get credentials
    credentials = Config.get_credentials()
    print(f"Credentials loaded: {credentials is not None}")
    
    # Print info
    print(f"Service account email: {credentials.service_account_email}")
    
    return True

if __name__ == "__main__":
    test_credentials()