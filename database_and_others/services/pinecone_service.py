from typing import Dict, List, Optional
import pinecone
from ..config.settings import Config

class PineconeService:
    def __init__(self):
        self._config = Config.get_pinecone_config()
        self._init_pinecone()
        
    def _init_pinecone(self):
        """Initialize Pinecone client and connect to index"""
        pinecone.init(
            api_key=self._config["api_key"],
            environment=self._config["environment"]
        )
        
        # Create index if it doesn't exist
        if self._config["index_name"] not in pinecone.list_indexes():
            pinecone.create_index(
                name=self._config["index_name"],
                dimension=Config.VECTOR_DIMENSION,
                metric="cosine"
            )
            
        self.index = pinecone.Index(self._config["index_name"])
    
    def upsert_vectors(self, vectors: List[Dict]):
        """
        Upsert vectors to Pinecone
        vectors: List of dictionaries containing 'id', 'values', and 'metadata'
        """
        return self.index.upsert(vectors=vectors)
    
    def query_vectors(
        self, 
        query_vector: List[float],
        top_k: int = 5,
        filter: Optional[Dict] = None
    ) -> Dict:
        """
        Query vectors from Pinecone
        query_vector: Vector to query against
        top_k: Number of results to return
        filter: Optional metadata filter
        """
        return self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter
        )
    
    def delete_vectors(self, ids: List[str]):
        """Delete vectors by IDs"""
        return self.index.delete(ids=ids)
    
    def fetch_vectors(self, ids: List[str]) -> Dict:
        """Fetch specific vectors by IDs"""
        return self.index.fetch(ids=ids)
    
    def get_index_stats(self) -> Dict:
        """Get index statistics"""
        return self.index.describe_index_stats()