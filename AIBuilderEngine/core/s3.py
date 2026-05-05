import boto3
from botocore.exceptions import NoCredentialsError
from .config import settings


class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION
        )
        self.bucket = settings.S3_BUCKET

    def upload_file(self, file_data: bytes, object_name: str, content_type: str = "image/png") -> str:
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=object_name,
                Body=file_data,
                ContentType=content_type
            )
            return f"{settings.S3_PUBLIC_URL}/{self.bucket}/{object_name}"

        except Exception as e:
            print(f"❌ S3 Upload Error: {e}")
            return ""

s3_client = S3Client()
