# DataTrack KMRL - Document Processing System

Document management system for Kochi Metro Rail Limited (KMRL) with AI-powered document processing capabilities.

## Features

- **Document OCR:** Extract text from various document formats
- **Language Detection:** Auto-detect document language
- **Translation:** Translate documents between supported languages
- **Document Classification:** Automatically categorize documents into KMRL-specific categories
- **Responsive Web Interface:** Modern UI for document management

## Architecture

The system consists of three main components:

1. **AI Services:** API for document processing with OCR, translation, and classification capabilities
2. **Backend Server:** API for document management, user authentication, and storage
3. **Frontend Client:** Web UI for user interaction

## Technology Stack

- **AI Services:** FastAPI, Google Cloud Vision API, Google Cloud Translation API, Google Cloud Natural Language API
- **Backend:** Node.js, Express, Prisma ORM, PostgreSQL
- **Frontend:** Next.js, React, Tailwind CSS, Shadcn/UI

## API Endpoints

### Document Processing Endpoint

```
POST /api/documents/process
```

Process a document with OCR, language detection, translation, and classification.

**Parameters:**
- `file`: Document image file
- `ocr_method`: 'document' (recommended) or 'text'
- `target_language`: Language for translation (default: 'en')
- `include_translation`: Whether to include translation in processing (default: false)
- `include_classification`: Whether to include document classification in processing (default: false)

**Response:**
```json
{
  "success": true,
  "data": {
    "processing_info": {
      "filename": "sample.jpg",
      "file_size": 123456,
      "upload_timestamp": "2023-08-15T10:30:15.123Z",
      "processing_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "processing_time_seconds": 2.45,
      "success": true,
      "errors": []
    },
    "ocr": {
      "text": "Extracted document text...",
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
    "translation": {
      "original_text": "Original text...",
      "translated_text": "Translated text...",
      "source_language": "ml",
      "target_language": "en",
      "source_language_name": "Malayalam",
      "target_language_name": "English",
      "error": null
    },
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

## Development Setup

1. Clone the repository
2. Set up environment variables (see `.env.example` files in each directory)
3. Install dependencies:
   ```bash
   # AI services
   cd ai-services
   pip install -r requirements.txt
   
   # Backend server
   cd server
   npm install
   
   # Frontend client
   cd client
   npm install
   ```
4. Run the services:
   ```bash
   # AI services
   cd ai-services
   python src/main.py
   
   # Backend server
   cd server
   npm run dev
   
   # Frontend client
   cd client
   npm run dev
   ```

## Testing

See the `tests` directory in each component for testing instructions.

For testing the document classification integration within the document processing pipeline, refer to `ai-services/tests/test_document_processing_with_classification.md`.

## Docker Deployment

Use the provided Docker Compose configuration to deploy the entire stack:

```bash
docker-compose up -d
```
