import boto3
import logging
from typing import Optional, Dict
from botocore.exceptions import ClientError, NoCredentialsError
from app.core.config import settings

logger = logging.getLogger(__name__)

class S3Service:
    """
    Servicio para simular interacción con AWS S3.
    Demuestra la lógica de conexión y manejo de excepciones con boto3.
    """
    
    def __init__(self):
        """
        Inicializa el cliente S3 con las credenciales de configuración.
        """
        try:
            self.s3_client = boto3.client(
                's3',
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            self.bucket_name = settings.AWS_S3_BUCKET
            logger.info(f"✓ Cliente S3 inicializado para bucket: {self.bucket_name}")
        except NoCredentialsError:
            logger.error("✗ Credenciales de AWS no encontradas")
            raise
        except Exception as e:
            logger.error(f"✗ Error al inicializar cliente S3: {str(e)}")
            raise

    def simulate_upload_maintenance_image(self, image_name: str, maintenance_id: int) -> Dict:
        """
        SIMULA la subida de una imagen de mantenimiento a S3.
        (Sin necesidad de archivo real)
        
        Args:
            image_name: Nombre de la imagen (ej: "IMG001.jpg")
            maintenance_id: ID del mantenimiento
        
        Returns:
            Dict con información de la simulación
        """
        try:
            object_key = f"maintenance/{maintenance_id}/{image_name}"
            
            logger.info(f"📤 Simulando subida a S3://{self.bucket_name}/{object_key}")
            
            # SIMULACIÓN: Verificar que el bucket exista (lógica)
            self._verify_bucket_exists()
            
            # SIMULACIÓN: Validar parámetros
            self._validate_image_name(image_name)
            
            # SIMULACIÓN: Construir URL S3
            s3_url = f"s3://{self.bucket_name}/{object_key}"
            
            logger.info(f"✓ Simulación exitosa. URL: {s3_url}")
            
            return {
                "status": "success",
                "message": "Imagen simulada correctamente",
                "s3_url": s3_url,
                "object_key": object_key,
                "bucket": self.bucket_name,
                "region": settings.AWS_REGION
            }
            
        except ValueError as e:
            logger.error(f"✗ Validación fallida: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"✗ Error en simulación: {str(e)}")
            raise

    def simulate_list_maintenance_images(self, maintenance_id: int) -> Dict:
        """
        SIMULA la listación de imágenes de un mantenimiento en S3.
        
        Args:
            maintenance_id: ID del mantenimiento
        
        Returns:
            Dict con lista simulada de imágenes
        """
        try:
            prefix = f"maintenance/{maintenance_id}/"
            
            logger.info(f"📋 Simulando listación de S3://{self.bucket_name}/{prefix}")
            
            # SIMULACIÓN: Verificar bucket
            self._verify_bucket_exists()
            
            # SIMULACIÓN: Datos simulados
            simulated_images = [
                f"{prefix}IMG001.jpg",
                f"{prefix}IMG002.jpg",
                f"{prefix}IMG003.jpg",
            ]
            
            logger.info(f"✓ Listación simulada. Total: {len(simulated_images)} imágenes")
            
            return {
                "status": "success",
                "bucket": self.bucket_name,
                "prefix": prefix,
                "total_images": len(simulated_images),
                "images": simulated_images
            }
            
        except Exception as e:
            logger.error(f"✗ Error en listación: {str(e)}")
            raise

    def simulate_delete_maintenance_image(self, image_path: str) -> Dict:
        """
        SIMULA la eliminación de una imagen de S3.
        
        Args:
            image_path: Ruta del archivo en S3
        
        Returns:
            Dict con resultado de la simulación
        """
        try:
            logger.info(f"🗑️  Simulando eliminación de S3://{self.bucket_name}/{image_path}")
            
            # SIMULACIÓN: Verificar bucket
            self._verify_bucket_exists()
            
            # SIMULACIÓN: Validar ruta
            if not image_path or len(image_path) < 5:
                raise ValueError("Ruta de imagen inválida")
            
            logger.info(f"✓ Simulación de eliminación exitosa")
            
            return {
                "status": "success",
                "message": f"Imagen {image_path} eliminada (simulado)",
                "bucket": self.bucket_name,
                "deleted_object": image_path
            }
            
        except ValueError as e:
            logger.error(f"✗ Validación fallida: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"✗ Error en eliminación: {str(e)}")
            raise

    def get_bucket_info(self) -> Dict:
        """
        Obtiene información del bucket configurado.
        Demuestra manejo de excepciones de AWS.
        """
        try:
            logger.info(f"ℹ️  Obteniendo información del bucket: {self.bucket_name}")
            
            # Intentar obtener información real (puede fallar si no existen credenciales)
            try:
                response = self.s3_client.head_bucket(Bucket=self.bucket_name)
                logger.info(f"✓ Bucket encontrado y accesible")
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == '404':
                    logger.warning(f"⚠️  Bucket no existe: {self.bucket_name}")
                    raise ValueError(f"El bucket {self.bucket_name} no existe")
                elif error_code == 'Forbidden':
                    logger.warning(f"⚠️  Acceso denegado al bucket")
                    raise PermissionError("No tienes permisos para acceder al bucket")
                else:
                    raise
            
            return {
                "status": "success",
                "bucket_name": self.bucket_name,
                "region": settings.AWS_REGION,
                "accessible": True
            }
            
        except NoCredentialsError:
            logger.error("✗ Credenciales de AWS no disponibles")
            raise
        except Exception as e:
            logger.error(f"✗ Error al obtener información del bucket: {str(e)}")
            raise

    # Métodos privados para simulación

    def _verify_bucket_exists(self) -> bool:
        """
        SIMULACIÓN: Verifica que el bucket exista.
        """
        if not self.bucket_name:
            raise ValueError("Nombre de bucket no configurado")
        logger.debug(f"✓ Bucket validado: {self.bucket_name}")
        return True

    def _validate_image_name(self, image_name: str) -> bool:
        """
        SIMULACIÓN: Valida el nombre de la imagen.
        """
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        import os
        _, ext = os.path.splitext(image_name)
        
        if ext.lower() not in allowed_extensions:
            raise ValueError(f"Extensión no permitida: {ext}. Usa: {allowed_extensions}")
        
        if len(image_name) > 255:
            raise ValueError("Nombre de archivo demasiado largo")
        
        logger.debug(f"✓ Nombre de imagen validado: {image_name}")
        return True


# Instancia singleton
s3_service = S3Service()

