# DataTrack KMRL - API Documentation

## AI Services API

The AI Services component provides document processing capabilities through a RESTful API.

### Base URL

```
http://localhost:8001
```

### Authentication

Currently, the AI Services API does not require authentication. When integrating with the backend server, authentication will be handled at that level.

### Common Response Format

All API responses follow this common structure:

```json
{
  "success": true|false,
  "data": { ... },  // Only present if success is true
  "error": { ... }  // Only present if success is false
}
```

### Endpoints

#### Health Check

```
GET /health
```

Returns the health status of the service.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "uptime": "2h 15m 30s"
}
```

#### Document Processing

```
POST /api/documents/process
```

Process a document with OCR, language detection, translation, and classification.

**Parameters:**
- `file`: Document image file (required)
- `ocr_method`: 'document' (recommended for structured documents) or 'text' (for simple text extraction)
- `target_language`: Language code for translation (default: 'en')
- `include_translation`: Whether to include translation in processing (default: false)
- `include_classification`: Whether to include document classification in processing (default: false)

**Response:**
```json
{
  "success": true,
  "data": {
    "processing_info": {
      "filename": "safety_report.jpg",
      "file_size": 245789,
      "upload_timestamp": "2023-08-15T10:30:15.123Z",
      "processing_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "processing_time_seconds": 2.45,
      "success": true,
      "errors": []
    },
    "ocr": {
      "text": "SAFETY REPORT\n\nDate: 2023-07-15\nLocation: Aluva Station\n\nIncident Description: Minor electrical fault detected in the control panel...",
      "confidence": 0.98,
      "method": "document",
      "error": null
    },
    "language_detection": {
      "language_code": "en",
      "language_name": "English",
      "confidence": 0.99,
      "error": null
    },
    "translation": null,  // Null if include_translation is false or language is already English
    "classification": {
      "category": "Safety circulars",
      "category_name": "Safety circulars", 
      "confidence": 0.85,
      "department": "Safety",
      "priority": "high",
      "error": null
    }
  }
}
```

#### OCR Only

```
POST /api/ocr/extract-text
```

Extract text from a document image.

**Parameters:**
- `file`: Document image file (required)
- `ocr_method`: 'document' (recommended) or 'text'

**Response:**
```json
{
  "success": true,
  "data": {
    "text": "Extracted document text...",
    "confidence": 0.98,
    "method": "document",
    "processing_time_seconds": 1.23,
    "character_count": 1250,
    "word_count": 215
  },
  "metadata": {
    "filename": "document.jpg",
    "file_size": 153246,
    "processed_at": "2023-08-15T10:30:15.123Z"
  }
}
```

#### Language Detection

```
POST /api/language/detect
```

Detect the language of text.

**Parameters:**
- `text`: Text content to analyze (required)

**Response:**
```json
{
  "success": true,
  "data": {
    "language_code": "ml",
    "language_name": "Malayalam",
    "confidence": 0.97,
    "is_kmrl_primary": true
  }
}
```

#### Translation

```
POST /api/translation/translate
```

Translate text between languages.

**Parameters:**
- `text`: Text to translate (required)
- `target_language`: Target language code (default: 'en')
- `source_language`: Source language code (optional, auto-detected if not provided)

**Response:**
```json
{
  "success": true,
  "data": {
    "original_text": "കേരള മെട്രോ റെയിൽ ലിമിറ്റഡ്",
    "translated_text": "Kochi Metro Rail Limited",
    "source_language": "ml",
    "target_language": "en",
    "source_language_name": "Malayalam",
    "target_language_name": "English",
    "error": null
  }
}
```

#### Document Classification

```
POST /api/classification/document
```

Classify a document based on its text content.

**Parameters:**
- `text`: Document text content (required)
- `min_confidence`: Minimum confidence threshold (default: 0.0)

**Response:**
```json
{
  "category": "Safety circulars",
  "confidence": 0.85,
  "all_categories": [
    {
      "category": "Safety circulars",
      "confidence": 0.85,
      "google_category": "/Health/Health & Safety"
    },
    {
      "category": "Incident reports",
      "confidence": 0.12,
      "google_category": "/Law & Government/Public Safety"
    }
  ],
  "processing_time_seconds": 0.35,
  "method": "google-cloud-natural-language"
}
```

#### Supported Languages

```
GET /api/languages
```

Get a list of supported languages for translation.

**Response:**
```json
{
  "success": true,
  "data": {
    "languages": [
      {
        "code": "en",
        "name": "English"
      },
      {
        "code": "ml",
        "name": "Malayalam"
      },
      // ... other languages
    ],
    "kmrl_primary": ["English", "Malayalam"],
    "total_count": 108
  }
}
```

## Error Handling

When an error occurs, the API returns an error response with an appropriate HTTP status code:

```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Invalid file type: application/pdf. Only images are supported."
  }
}
```

Common error status codes:
- 400: Bad Request (invalid input)
- 404: Not Found (endpoint doesn't exist)
- 500: Internal Server Error (processing failure)

## Rate Limiting

Currently, there are no rate limits implemented for the AI Services API.
