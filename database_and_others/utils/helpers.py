from typing import Dict, List
import uuid
import datetime

def generate_unique_id() -> str:
    """Generate a unique ID for document storage"""
    return str(uuid.uuid4())

def create_document_metadata(
    filename: str,
    file_type: str,
    s3_key: str,
    additional_metadata: Dict = None
) -> Dict:
    """Create metadata for document storage"""
    metadata = {
        "filename": filename,
        "file_type": file_type,
        "s3_key": s3_key,
        "upload_date": datetime.datetime.utcnow().isoformat(),
        "source": "datatrack-kmrl"
    }
    
    if additional_metadata:
        metadata.update(additional_metadata)
    
    return metadata

def create_vector_record(
    vector: List[float],
    metadata: Dict,
    doc_id: str = None
) -> Dict:
    """Create a vector record for Pinecone storage"""
    if not doc_id:
        doc_id = generate_unique_id()
        
    return {
        "id": doc_id,
        "values": vector,
        "metadata": metadata
    }