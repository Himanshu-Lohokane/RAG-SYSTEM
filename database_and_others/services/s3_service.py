from typing import Dict, Optional, BinaryIO
import boto3
from botocore.exceptions import ClientError
from ..config.settings import Config

class S3Service:
    def __init__(self):
        self._config = Config.get_s3_config()
        self._init_s3()
        
    def _init_s3(self):
        """Initialize S3 client"""
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self._config["aws_access_key_id"],
            aws_secret_access_key=self._config["aws_secret_access_key"],
            region_name=self._config["region_name"]
        )
        self.bucket_name = self._config["bucket_name"]
        
    def upload_file(
        self,
        file_obj: BinaryIO,
        s3_key: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Upload a file to S3
        file_obj: File object to upload
        s3_key: The key (path) where the file will be stored in S3
        metadata: Optional metadata to attach to the file
        """
        try:
            extra_args = {"Metadata": metadata} if metadata else {}
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                s3_key,
                ExtraArgs=extra_args
            )
            
            # Generate a presigned URL for temporary access
            url = self.generate_presigned_url(s3_key)
            
            return {
                "status": "success",
                "s3_key": s3_key,
                "url": url,
                "bucket": self.bucket_name
            }
        except ClientError as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def download_file(self, s3_key: str) -> Optional[bytes]:
        """Download a file from S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return response['Body'].read()
        except ClientError:
            return None
    
    def generate_presigned_url(
        self,
        s3_key: str,
        expiration: int = 3600
    ) -> Optional[str]:
        """Generate a presigned URL for temporary file access"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError:
            return None
    
    def delete_file(self, s3_key: str) -> bool:
        """Delete a file from S3"""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        except ClientError:
            return False
    
    def get_file_metadata(self, s3_key: str) -> Optional[Dict]:
        """Get file metadata from S3"""
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return response.get('Metadata', {})