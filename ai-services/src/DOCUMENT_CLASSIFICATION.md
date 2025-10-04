# Document Classification with Google Cloud Natural Language API

This implementation uses Google Cloud Natural Language API for document classification without requiring custom training or document samples. It's a more sophisticated approach than keyword matching but doesn't require building a custom classifier.

## Overview

The solution uses Google's pre-trained content classification models through the Natural Language API to analyze document text and classify it into appropriate categories. The implementation includes:

1. Primary classification using Google Cloud Natural Language API
2. Mapping of Google's categories to KMRL-specific document categories
3. Fallback to keyword-based classification if the API is unavailable

## Benefits

- No need for custom training data or labeled documents
- More sophisticated than keyword matching
- Leverages Google's powerful pre-trained models
- Can classify documents in multiple languages
- Provides confidence scores for each category
- Falls back gracefully if the API is unavailable

## How It Works

1. Document text is sent to Google Cloud Natural Language API
2. The API returns content categories with confidence scores
3. These categories are mapped to KMRL-specific document categories
4. The system selects the best matching KMRL category based on confidence scores
5. If the API is unavailable, the system falls back to keyword matching

## Sample Request

```bash
curl -X POST "http://localhost:8001/classify/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a safety protocol document for handling equipment in the metro station."}'
```

## Sample Response

```json
{
  "category": "Safety circulars",
  "confidence": 0.87,
  "all_categories": [
    {
      "category": "Safety circulars",
      "google_category": "/Health/Health & Safety",
      "confidence": 0.87
    },
    {
      "category": "Incident reports",
      "google_category": "/Law & Government/Public Safety",
      "confidence": 0.42
    }
  ],
  "google_categories": [
    {
      "name": "/Health/Health & Safety",
      "confidence": 0.87
    },
    {
      "name": "/Law & Government/Public Safety",
      "confidence": 0.42
    }
  ],
  "method": "google-cloud-natural-language",
  "processing_time_seconds": 0.856
}
```

## Setup

1. Ensure you have Google Cloud credentials properly set up
2. Install the required packages:
   ```
   pip install google-cloud-language>=2.13.1
   ```

## Testing

You can use the included `sample_classify.py` script to test the classification:

```
python src/sample_classify.py [optional_text_file.txt]
```

If no file is provided, the script will run with sample texts for different document types.

## API Endpoints

- **POST /classify/text**: Classify document based on provided text content
- **POST /api/classification/document**: Upload a document for OCR and classification
- **POST /api/classification/text**: Legacy endpoint for text classification

## Google Cloud Natural Language API Documentation

For more information on the Google Cloud Natural Language API:
https://cloud.google.com/natural-language/docs/