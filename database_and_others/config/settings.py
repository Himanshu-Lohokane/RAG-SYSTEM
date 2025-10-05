from typing import Dict
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Pinecone Configuration
    PINECONE_API_KEY: str = "pcsk_3vcAYi_NTrwEwryNu3dmwyEiv9cvc5JwdCmiAKMuSsGwUMhfcd7qngkpLEXZfCiUzfDpG5"
    PINECONE_ENVIRONMENT: str = "gcp-starter"  # Update this with your environment
    PINECONE_INDEX_NAME: str = "datatrack-kmrl"  # Update this with your index name
    
    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")  # Update with your preferred region
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "datatrack-kmrl-documents")  # Update with your bucket name
    
    # Vector Configuration
    VECTOR_DIMENSION: int = 1536  # Using OpenAI's ada-002 dimension
    
    @staticmethod
    def get_pinecone_config() -> Dict:
        return {
            "api_key": Config.PINECONE_API_KEY,
            "environment": Config.PINECONE_ENVIRONMENT,
            "index_name": Config.PINECONE_INDEX_NAME
        }
    
    @staticmethod
    def get_s3_config() -> Dict:
        return {
            "aws_access_key_id": Config.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": Config.AWS_SECRET_ACCESS_KEY,
            "region_name": Config.AWS_REGION,
            "bucket_name": Config.S3_BUCKET_NAME
        }