# Testing Document Classification in the Processing Endpoint

This document outlines how to test the integration of document classification within the document processing endpoint.

## Test Scenarios

### 1. Basic OCR Only (No Classification)

```bash
# Command
curl -X POST "http://localhost:8001/api/documents/process" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@./sample.jpg" \
     -F "ocr_method=document" \
     -F "include_classification=false"
```

Expected outcome: The API responds with OCR results and language detection, but no classification results.

### 2. OCR with Classification

```bash
# Command
curl -X POST "http://localhost:8001/api/documents/process" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@./sample.jpg" \
     -F "ocr_method=document" \
     -F "include_classification=true"
```

Expected outcome: The API responds with OCR results, language detection, and classification results including the document category and confidence score.

### 3. Full Processing Pipeline (OCR + Translation + Classification)

```bash
# Command
curl -X POST "http://localhost:8001/api/documents/process" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@./sample.jpg" \
     -F "ocr_method=document" \
     -F "include_translation=true" \
     -F "target_language=en" \
     -F "include_classification=true"
```

Expected outcome: The API responds with OCR results, language detection, translation (if not English), and classification results.

### 4. Test with Different Document Types

Test the endpoint with different document types from the sample-documents directory:
- Engineering documents
- Financial documents 
- HR documents
- Safety documents
- Multilingual documents

### 5. Python Test Script

```python
import requests
import json
import os

# API endpoint URL
url = "http://localhost:8001/api/documents/process"

# Test with different sample documents
sample_dirs = [
    "data/sample-documents/engineering",
    "data/sample-documents/financial",
    "data/sample-documents/hr",
    "data/sample-documents/safety",
    "data/sample-documents/multilingual"
]

for sample_dir in sample_dirs:
    print(f"\nTesting documents in {sample_dir}")
    
    # List files in the directory
    files = os.listdir(sample_dir)
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
            file_path = os.path.join(sample_dir, file)
            print(f"\n- Testing {file_path}")
            
            # Prepare the file for upload
            with open(file_path, 'rb') as f:
                files = {'file': (file, f, 'image/jpeg')}
                
                # Set parameters
                data = {
                    'ocr_method': 'document',
                    'include_translation': 'true',
                    'target_language': 'en',
                    'include_classification': 'true'
                }
                
                # Send the request
                response = requests.post(url, files=files, data=data)
                
                # Check the response
                if response.status_code == 200:
                    result = response.json()
                    
                    # Print classification result
                    classification = result.get('data', {}).get('classification')
                    if classification:
                        print(f"   Classification: {classification['category']} (Confidence: {classification['confidence']:.2f})")
                    else:
                        print("   No classification result found")
                else:
                    print(f"   Error: {response.status_code} - {response.text}")
```

## Verification Checklist

1. Ensure that classification only happens when `include_classification=true`
2. Verify that classification results include:
   - Category
   - Confidence score
   - No errors
3. Confirm that classification works correctly for both:
   - Original text (when no translation is needed/requested)
   - Translated text (when translation is performed)
4. Check that classification is skipped if OCR fails
5. Validate performance impact of adding classification (processing time)