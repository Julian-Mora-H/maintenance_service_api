from fastapi import APIRouter, HTTPException, status
from app.services.s3_service import s3_service
from app.utils.decorators import measure_time
from pydantic import BaseModel

router = APIRouter()

class MaintenanceImageSimulation(BaseModel):
    """Simulation payload for image upload"""
    image_name: str
    maintenance_id: int

@router.post("/simulate-upload-image")
@measure_time
def simulate_upload_maintenance_image(data: MaintenanceImageSimulation):
    """
    Simulates uploading a maintenance image to S3.

    No real file required, only demonstrates boto3 logic.
    """
    try:
        result = s3_service.simulate_upload_maintenance_image(
            data.image_name,
            data.maintenance_id
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/simulate-list-images/{maintenance_id}")
@measure_time
def simulate_list_maintenance_images(maintenance_id: int):
    """
    Simulates listing maintenance images in S3.

    Does not access real S3, returns simulated data only.
    """
    try:
        result = s3_service.simulate_list_maintenance_images(maintenance_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/simulate-delete-image")
@measure_time
def simulate_delete_maintenance_image(image_path: str):
    """
    Simulates deleting an image from S3.

    Demonstrates exception handling without real S3 access.
    """
    try:
        result = s3_service.simulate_delete_maintenance_image(image_path)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/bucket-info")
@measure_time
def get_bucket_info():
    """
    Retrieves info for the configured S3 bucket.

    Demonstrates real AWS connection and exception handling.
    """
    try:
        result = s3_service.get_bucket_info()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
