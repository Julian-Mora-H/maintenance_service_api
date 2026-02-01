import boto3
import logging
from typing import Optional, Dict
from botocore.exceptions import ClientError, NoCredentialsError
from app.core.config import settings

logger = logging.getLogger(__name__)

class S3Service:
    """
    Service to simulate AWS S3 interaction.
    Demonstrates connection logic and exception handling with boto3.
    """
    
    def __init__(self):
        """
        Initialize S3 client with configured credentials.
        """
        try:
            self.s3_client = boto3.client(
                's3',
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            self.bucket_name = settings.AWS_S3_BUCKET
            logger.info(f"✓ S3 client initialized for bucket: {self.bucket_name}")
        except NoCredentialsError:
            logger.error("✗ AWS credentials not found")
            raise
        except Exception as e:
            logger.error(f"✗ Error initializing S3 client: {str(e)}")
            raise

    def simulate_upload_maintenance_image(self, image_name: str, maintenance_id: int) -> Dict:
        """
        Simulates uploading a maintenance image to S3.
        (No real file required)

        Args:
            image_name: Image name (e.g., "IMG001.jpg")
            maintenance_id: Maintenance ID

        Returns:
            Dict with simulation details
        """
        try:
            object_key = f"maintenance/{maintenance_id}/{image_name}"
            
            logger.info(f"📤 Simulating upload to S3://{self.bucket_name}/{object_key}")
            
            # SIMULATION: Verify bucket exists (logic)
            self._verify_bucket_exists()
            
            # SIMULATION: Validate parameters
            self._validate_image_name(image_name)
            
            # SIMULATION: Build S3 URL
            s3_url = f"s3://{self.bucket_name}/{object_key}"
            
            logger.info(f"✓ Simulation successful. URL: {s3_url}")
            
            return {
                "status": "success",
                "message": "Image simulated successfully",
                "s3_url": s3_url,
                "object_key": object_key,
                "bucket": self.bucket_name,
                "region": settings.AWS_REGION
            }
            
        except ValueError as e:
            logger.error(f"✗ Validation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"✗ Simulation error: {str(e)}")
            raise

    def simulate_list_maintenance_images(self, maintenance_id: int) -> Dict:
        """
        Simulates listing maintenance images in S3.

        Args:
            maintenance_id: Maintenance ID

        Returns:
            Dict with simulated image list
        """
        try:
            prefix = f"maintenance/{maintenance_id}/"
            
            logger.info(f"📋 Simulating listing of S3://{self.bucket_name}/{prefix}")
            
            # SIMULATION: Verify bucket
            self._verify_bucket_exists()
            
            # SIMULATION: Simulated data
            simulated_images = [
                f"{prefix}IMG001.jpg",
                f"{prefix}IMG002.jpg",
                f"{prefix}IMG003.jpg",
            ]
            
            logger.info(f"✓ Simulated listing. Total: {len(simulated_images)} images")
            
            return {
                "status": "success",
                "bucket": self.bucket_name,
                "prefix": prefix,
                "total_images": len(simulated_images),
                "images": simulated_images
            }
            
        except Exception as e:
            logger.error(f"✗ Listing error: {str(e)}")
            raise

    def simulate_delete_maintenance_image(self, image_path: str) -> Dict:
        """
        Simulates deleting an image from S3.

        Args:
            image_path: S3 object path

        Returns:
            Dict with simulation result
        """
        try:
            logger.info(f"🗑️  Simulating deletion of S3://{self.bucket_name}/{image_path}")
            
            # SIMULATION: Verify bucket
            self._verify_bucket_exists()
            
            # SIMULATION: Validate path
            if not image_path or len(image_path) < 5:
                raise ValueError("Invalid image path")
            
            logger.info("✓ Deletion simulation successful")
            
            return {
                "status": "success",
                "message": f"Image {image_path} deleted (simulated)",
                "bucket": self.bucket_name,
                "deleted_object": image_path
            }
            
        except ValueError as e:
            logger.error(f"✗ Validation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"✗ Deletion error: {str(e)}")
            raise

    def get_bucket_info(self) -> Dict:
        """
        Get info about the configured bucket.
        Demonstrates AWS exception handling.
        """
        try:
            logger.info(f"ℹ️  Getting bucket info: {self.bucket_name}")
            
            # Try to fetch real info (may fail if credentials are missing)
            try:
                response = self.s3_client.head_bucket(Bucket=self.bucket_name)
                logger.info("✓ Bucket found and accessible")
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == '404':
                    logger.warning(f"⚠️  Bucket does not exist: {self.bucket_name}")
                    raise ValueError(f"Bucket {self.bucket_name} does not exist")
                elif error_code == 'Forbidden':
                    logger.warning("⚠️  Access denied to bucket")
                    raise PermissionError("No permission to access the bucket")
                else:
                    raise
            
            return {
                "status": "success",
                "bucket_name": self.bucket_name,
                "region": settings.AWS_REGION,
                "accessible": True
            }
            
        except NoCredentialsError:
            logger.error("✗ AWS credentials not available")
            raise
        except Exception as e:
            logger.error(f"✗ Error getting bucket info: {str(e)}")
            raise

    # Private helpers for simulation

    def _verify_bucket_exists(self) -> bool:
        """
        SIMULATION: Verify that the bucket exists.
        """
        if not self.bucket_name:
            raise ValueError("Bucket name not configured")
        logger.debug(f"✓ Bucket validated: {self.bucket_name}")
        return True

    def _validate_image_name(self, image_name: str) -> bool:
        """
        SIMULATION: Validate image name.
        """
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        import os
        _, ext = os.path.splitext(image_name)
        
        if ext.lower() not in allowed_extensions:
            raise ValueError(f"Extension not allowed: {ext}. Use: {allowed_extensions}")
        
        if len(image_name) > 255:
            raise ValueError("File name too long")
        
        logger.debug(f"✓ Image name validated: {image_name}")
        return True


# Instancia singleton
s3_service = S3Service()

