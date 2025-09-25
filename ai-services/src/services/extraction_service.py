# DataTrack KMRL - Entity Extraction Service
# Extract structured data from documents (entities, key-value pairs, tables, etc.)

import os
import sys
import re
import time
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel
from datetime import datetime
from google.cloud import language_v1
import json

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config

class EntityResult(BaseModel):
    """Entity extraction result from a document"""
    name: str
    type: str
    salience: float
    mentions: List[Dict[str, Any]]
    metadata: Dict[str, Any] = {}

class EntityExtractionResult(BaseModel):
    """Complete entity extraction result"""
    entities: List[EntityResult]
    language: str
    text: str
    error: Optional[str] = None

class KeyValuePair(BaseModel):
    """Key-value pair extracted from documents"""
    key: str
    value: str
    confidence: float
    bounding_box: Optional[Dict[str, Any]] = None

class KeyValueExtractionResult(BaseModel):
    """Complete key-value extraction result"""
    pairs: List[KeyValuePair]
    language: str
    text: str
    error: Optional[str] = None

class TableCell(BaseModel):
    """Cell in an extracted table"""
    row_idx: int
    col_idx: int
    text: str
    confidence: float
    bounding_box: Optional[Dict[str, Any]] = None

class Table(BaseModel):
    """Table extracted from a document"""
    rows: int
    columns: int
    cells: List[TableCell]
    text: Optional[str] = None
    confidence: float
    bounding_box: Optional[Dict[str, Any]] = None

class TableExtractionResult(BaseModel):
    """Complete table extraction result"""
    tables: List[Table]
    page_count: int
    raw_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class FormField(BaseModel):
    """Field extracted from a form"""
    name: str
    value: str
    confidence: float
    type: str
    bounding_box: Optional[Dict[str, Any]] = None

class FormExtractionResult(BaseModel):
    """Complete form extraction result"""
    fields: List[FormField]
    form_type: Optional[str] = None
    page_count: int
    confidence: float
    error: Optional[str] = None

class EntityExtractionService:
    """Service to extract structured data from documents"""
    
    def __init__(self):
        """Initialize extraction services"""
        print("[EXTRACT] Initializing Google Cloud Natural Language client for entity extraction...")
        self.nlp_client = language_v1.LanguageServiceClient()
        print("[EXTRACT] ✅ Entity extraction service ready")
    
    def extract_entities(self, text: str, language: str = "en") -> EntityExtractionResult:
        """
        Extract entities from text using Google NL API
        
        Args:
            text: The text to analyze
            language: Language code (en, ml)
            
        Returns:
            EntityExtractionResult with extracted entities
        """
        print(f"[EXTRACT] Analyzing entities in text ({len(text)} chars, language: {language})")
        
        try:
            # Create document for analysis
            document = language_v1.Document(
                content=text,
                language=language,
                type_=language_v1.Document.Type.PLAIN_TEXT
            )
            
            # Detect entities
            start_time = time.time()
            entity_response = self.nlp_client.analyze_entities(
                document=document,
                encoding_type=language_v1.EncodingType.UTF8
            )
            processing_time = time.time() - start_time
            
            # Convert entities to result format
            entities = []
            for entity in entity_response.entities:
                entity_data = EntityResult(
                    name=entity.name,
                    type=language_v1.Entity.Type(entity.type_).name,
                    salience=entity.salience,
                    mentions=[{
                        "text": mention.text.content,
                        "type": language_v1.EntityMention.Type(mention.type_).name,
                        "begin_offset": mention.text.begin_offset
                    } for mention in entity.mentions],
                    metadata={key: value for key, value in entity.metadata.items()}
                )
                entities.append(entity_data)
            
            print(f"[EXTRACT] ✅ Extracted {len(entities)} entities in {processing_time:.2f}s")
            
            return EntityExtractionResult(
                entities=entities,
                language=language,
                text=text[:100] + "..." if len(text) > 100 else text  # Truncate for logs
            )
            
        except Exception as e:
            error_msg = f"Entity extraction failed: {str(e)}"
            print(f"[EXTRACT] ❌ {error_msg}")
            
            return EntityExtractionResult(
                entities=[],
                language=language,
                text=text[:100] + "..." if len(text) > 100 else text,
                error=error_msg
            )
    
    def extract_key_value_pairs(self, text: str, language: str = "en") -> KeyValueExtractionResult:
        """
        Extract key-value pairs from text using regex and NLP
        
        Args:
            text: The text to analyze
            language: Language code (en, ml)
            
        Returns:
            KeyValueExtractionResult with extracted pairs
        """
        print(f"[EXTRACT] Extracting key-value pairs from text ({len(text)} chars)")
        
        try:
            # Simple regex-based extraction for demo purposes
            # In production, would use DocumentAI or more advanced techniques
            
            # Pattern for "Key: Value" or "Key - Value"
            kv_patterns = [
                r'([A-Za-z\s]+?):\s*(.+?)(?=\n|$)',  # Key: Value
                r'([A-Za-z\s]+?)\s*-\s*(.+?)(?=\n|$)',  # Key - Value
                r'([A-Za-z\s]+?)=\s*(.+?)(?=\n|$)',  # Key=Value
            ]
            
            pairs = []
            
            for pattern in kv_patterns:
                matches = re.finditer(pattern, text)
                
                for match in matches:
                    key = match.group(1).strip()
                    value = match.group(2).strip()
                    
                    # Skip if key or value is too short
                    if len(key) < 2 or len(value) < 1:
                        continue
                    
                    # Skip if key is too long (likely not a key)
                    if len(key) > 50:
                        continue
                    
                    # Add to results
                    pairs.append(KeyValuePair(
                        key=key,
                        value=value,
                        confidence=0.85,  # Mock confidence since this is regex-based
                        bounding_box=None  # No bounding box for text-based extraction
                    ))
            
            print(f"[EXTRACT] ✅ Extracted {len(pairs)} key-value pairs")
            
            return KeyValueExtractionResult(
                pairs=pairs,
                language=language,
                text=text[:100] + "..." if len(text) > 100 else text,
                error=None
            )
            
        except Exception as e:
            error_msg = f"Key-value extraction failed: {str(e)}"
            print(f"[EXTRACT] ❌ {error_msg}")
            
            return KeyValueExtractionResult(
                pairs=[],
                language=language,
                text=text[:100] + "..." if len(text) > 100 else text,
                error=error_msg
            )
    
    def extract_tables(self, image_data: bytes) -> TableExtractionResult:
        """
        Extract tables from document images
        
        Args:
            image_data: Image bytes containing tables
            
        Returns:
            TableExtractionResult with extracted tables
        """
        print(f"[EXTRACT] Table extraction requested (image size: {len(image_data)} bytes)")
        
        try:
            # TODO: Implement real table extraction with Document AI or similar
            # For demo, return mock table extraction results
            
            # Create mock table 1
            cells_1 = [
                TableCell(row_idx=0, col_idx=0, text="Item", confidence=0.98, 
                         bounding_box={"x": 10, "y": 10, "width": 100, "height": 30}),
                TableCell(row_idx=0, col_idx=1, text="Quantity", confidence=0.99,
                         bounding_box={"x": 120, "y": 10, "width": 100, "height": 30}),
                TableCell(row_idx=0, col_idx=2, text="Price", confidence=0.97,
                         bounding_box={"x": 230, "y": 10, "width": 100, "height": 30}),
                TableCell(row_idx=1, col_idx=0, text="Desk Lamp", confidence=0.95,
                         bounding_box={"x": 10, "y": 50, "width": 100, "height": 30}),
                TableCell(row_idx=1, col_idx=1, text="2", confidence=0.99,
                         bounding_box={"x": 120, "y": 50, "width": 100, "height": 30}),
                TableCell(row_idx=1, col_idx=2, text="₹1200", confidence=0.96,
                         bounding_box={"x": 230, "y": 50, "width": 100, "height": 30}),
                TableCell(row_idx=2, col_idx=0, text="Office Chair", confidence=0.94,
                         bounding_box={"x": 10, "y": 90, "width": 100, "height": 30}),
                TableCell(row_idx=2, col_idx=1, text="1", confidence=0.99,
                         bounding_box={"x": 120, "y": 90, "width": 100, "height": 30}),
                TableCell(row_idx=2, col_idx=2, text="₹5500", confidence=0.97,
                         bounding_box={"x": 230, "y": 90, "width": 100, "height": 30})
            ]
            
            table_1 = Table(
                rows=3,
                columns=3,
                cells=cells_1,
                text="Item Quantity Price\nDesk Lamp 2 ₹1200\nOffice Chair 1 ₹5500",
                confidence=0.95,
                bounding_box={"x": 10, "y": 10, "width": 320, "height": 110}
            )
            
            # Create mock table 2 
            cells_2 = [
                TableCell(row_idx=0, col_idx=0, text="Date", confidence=0.98,
                         bounding_box={"x": 10, "y": 150, "width": 100, "height": 30}),
                TableCell(row_idx=0, col_idx=1, text="Reference", confidence=0.97,
                         bounding_box={"x": 120, "y": 150, "width": 100, "height": 30}),
                TableCell(row_idx=1, col_idx=0, text="2023-05-12", confidence=0.96,
                         bounding_box={"x": 10, "y": 190, "width": 100, "height": 30}),
                TableCell(row_idx=1, col_idx=1, text="INV-2023-0542", confidence=0.95,
                         bounding_box={"x": 120, "y": 190, "width": 100, "height": 30})
            ]
            
            table_2 = Table(
                rows=2,
                columns=2,
                cells=cells_2,
                text="Date Reference\n2023-05-12 INV-2023-0542",
                confidence=0.96,
                bounding_box={"x": 10, "y": 150, "width": 220, "height": 70}
            )
            
            print(f"[EXTRACT] ✅ Table extraction completed (mock data for demo)")
            
            return TableExtractionResult(
                tables=[table_1, table_2],
                page_count=1,
                raw_data=None,
                error=None
            )
            
        except Exception as e:
            error_msg = f"Table extraction failed: {str(e)}"
            print(f"[EXTRACT] ❌ {error_msg}")
            
            return TableExtractionResult(
                tables=[],
                page_count=0,
                raw_data=None,
                error=error_msg
            )
    
    def extract_form_fields(self, image_data: bytes, form_template: Optional[str] = None) -> FormExtractionResult:
        """
        Extract form fields from document images
        
        Args:
            image_data: Image bytes containing form
            form_template: Optional template name for known form types
            
        Returns:
            FormExtractionResult with extracted fields
        """
        print(f"[EXTRACT] Form field extraction requested (image size: {len(image_data)} bytes)")
        
        try:
            # TODO: Implement real form field extraction with Document AI or similar
            # For demo, return mock form field extraction results
            
            # Create mock form fields based on template type
            if form_template == "invoice":
                fields = [
                    FormField(name="Invoice Number", value="INV-2023-0542", confidence=0.97, type="text",
                             bounding_box={"x": 400, "y": 50, "width": 150, "height": 30}),
                    FormField(name="Date", value="2023-05-12", confidence=0.95, type="date",
                             bounding_box={"x": 400, "y": 90, "width": 150, "height": 30}),
                    FormField(name="Customer", value="KMRL Metro Operations", confidence=0.93, type="text",
                             bounding_box={"x": 100, "y": 150, "width": 300, "height": 30}),
                    FormField(name="Total Amount", value="₹6700", confidence=0.96, type="amount",
                             bounding_box={"x": 400, "y": 400, "width": 150, "height": 30})
                ]
                form_type = "invoice"
            elif form_template == "purchase_order":
                fields = [
                    FormField(name="PO Number", value="PO-2023-1087", confidence=0.98, type="text",
                             bounding_box={"x": 400, "y": 50, "width": 150, "height": 30}),
                    FormField(name="Date", value="2023-05-10", confidence=0.96, type="date",
                             bounding_box={"x": 400, "y": 90, "width": 150, "height": 30}),
                    FormField(name="Vendor", value="Office Supplies Ltd", confidence=0.94, type="text",
                             bounding_box={"x": 100, "y": 150, "width": 300, "height": 30}),
                    FormField(name="Delivery Date", value="2023-05-20", confidence=0.92, type="date",
                             bounding_box={"x": 400, "y": 150, "width": 150, "height": 30}),
                    FormField(name="Total Amount", value="₹6700", confidence=0.95, type="amount",
                             bounding_box={"x": 400, "y": 400, "width": 150, "height": 30})
                ]
                form_type = "purchase_order"
            else:
                # Generic form fields
                fields = [
                    FormField(name="Name", value="John Smith", confidence=0.96, type="text",
                             bounding_box={"x": 200, "y": 100, "width": 300, "height": 30}),
                    FormField(name="Date", value="2023-05-15", confidence=0.97, type="date",
                             bounding_box={"x": 200, "y": 150, "width": 150, "height": 30}),
                    FormField(name="Address", value="123 Main St, Kochi", confidence=0.92, type="text",
                             bounding_box={"x": 200, "y": 200, "width": 300, "height": 60}),
                    FormField(name="Phone", value="+91-9876543210", confidence=0.95, type="phone",
                             bounding_box={"x": 200, "y": 270, "width": 200, "height": 30}),
                    FormField(name="Signature", value="[Signature detected]", confidence=0.85, type="signature",
                             bounding_box={"x": 200, "y": 400, "width": 200, "height": 60})
                ]
                form_type = "generic"
            
            print(f"[EXTRACT] ✅ Form field extraction completed (mock data for demo)")
            
            return FormExtractionResult(
                fields=fields,
                form_type=form_type,
                page_count=1,
                confidence=0.94,
                error=None
            )
            
        except Exception as e:
            error_msg = f"Form field extraction failed: {str(e)}"
            print(f"[EXTRACT] ❌ {error_msg}")
            
            return FormExtractionResult(
                fields=[],
                form_type=None,
                page_count=0,
                confidence=0.0,
                error=error_msg
            )
