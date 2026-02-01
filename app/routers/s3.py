from fastapi import APIRouter, HTTPException, status
from app.services.s3_service import s3_service
from app.utils.decorators import measure_time
from pydantic import BaseModel

router = APIRouter()

class MaintenanceImageSimulation(BaseModel):
    """Simulación de datos para subida de imagen"""
    image_name: str
    maintenance_id: int

@router.post("/simulate-upload-image")
@measure_time
def simulate_upload_maintenance_image(data: MaintenanceImageSimulation):
    """
    SIMULA la subida de una imagen de mantenimiento a S3.

    No requiere archivo real, solo demuestra la lógica con boto3.
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
    SIMULA la listación de imágenes de un mantenimiento en S3.

    No accede a S3 real, solo devuelve datos simulados.
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
    SIMULA la eliminación de una imagen de S3.

    Demuestra manejo de excepciones sin acceder a S3 real.
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
    Obtiene información del bucket S3 configurado.

    Demuestra la conexión real a AWS y manejo de excepciones.
    """
    try:
        result = s3_service.get_bucket_info()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
