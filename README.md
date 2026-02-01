# 🔧 Maintenance Service API

API FastAPI para gestión de órdenes de mantenimiento con integración a AWS S3.

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación Local](#instalación-local)
- [Ejecución del Proyecto](#ejecución-del-proyecto)
- [Documentación Swagger](#documentación-swagger)
- [Idempotencia en Órdenes](#idempotencia-en-órdenes)

## 📋 Requisitos Previos

- **Python 3.12+**
- **pip** (gestor de paquetes de Python)
- **Git** (para clonar el repositorio)
- **Windows/Linux/Mac** (compatible con todos los SO)

## 🚀 Instalación Local

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Maintenance_Service_API
```

### 2. Crear entorno virtual

**En Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**En Linux/Mac:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si no tienes `requirements.txt`, instala manualmente:
```bash
pip install fastapi uvicorn sqlalchemy pydantic-settings python-dotenv boto3 python-multipart pytest httpx
```

### 4. Variables de configuración (opcional)

No es necesario crear `.env` porque los valores por defecto están en [app/core/config.py](app/core/config.py).
Solo crea `.env` si quieres sobrescribirlos:

```env
PROJECT_NAME=Maintenance Service API
PROJECT_VERSION=0.1.0
DATABASE_URL=sqlite:///./maintenance.db
AWS_S3_BUCKET=mi-bucket-simulado
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
```

> **Nota**: Para desarrollo local, puedes usar valores simulados en las variables de AWS.

## ▶️ Ejecución del Proyecto

### Iniciar el servidor

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Deberías ver algo como:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Verificar que el servidor está corriendo

Abre tu navegador y accede a:
```
http://127.0.0.1:8000/docs
```

## 📚 Documentación Swagger

La API está completamente documentada con **Swagger (OpenAPI)** y está disponible automáticamente en:

**`http://127.0.0.1:8000/docs`**

En Swagger podrás:
- ✅ Ver todos los endpoints disponibles
- ✅ Probar las peticiones en tiempo real
- ✅ Ver esquemas de request/response
- ✅ Ver ejemplos de uso

## ✅ Pruebas

### Ejecutar pruebas unitarias

```bash
pytest
```

Si deseas usar el ejecutable del entorno virtual:

```bash
F:/PROYECTOS/CURSOS/Maintenance_Service_API/env/Scripts/python.exe -m pytest
```

### Qué se prueba

- Creación y listado de categorías
- Creación y listado de items con LEFT JOIN
- PATCH parcial de items
- Idempotencia en órdenes

### Endpoints Disponibles

#### **Items**
- `POST /router/items/` - Crear item
- `GET /router/items/` - Listar items
- `PATCH /router/items/{item_id}` - Actualizar item

#### **Categorías**
- `POST /router/categories/` - Crear categoría
- `GET /router/categories/` - Listar categorías
- `PATCH /router/categories/{category_id}` - Actualizar categoría

#### **Órdenes**
- `POST /router/orders/` - Crear orden (con **idempotencia**)
- `GET /router/orders/` - Listar órdenes

#### **S3 (Mantenimiento - Simulado)**
- `POST /router/s3/simulate-upload-image` - Simular subida de imagen
- `GET /router/s3/simulate-list-images/{maintenance_id}` - Listar imágenes simuladas
- `POST /router/s3/simulate-delete-image` - Simular eliminación de imagen
- `GET /router/s3/bucket-info` - Obtener información del bucket

## 🔐 Idempotencia en Órdenes

### ¿Qué es la Idempotencia?

La idempotencia garantiza que **si envías la misma petición varias veces, NO se duplicarán los datos**. La primera vez crea la orden, las siguientes devuelven la misma orden sin crear duplicados.

### ¿Cómo funciona?

#### **1. Usando Header `Idempotency-Key`** (Recomendado)

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/router/orders/' \
  -H 'Idempotency-Key: abc123' \
  -H 'Content-Type: application/json' \
  -d '{
    "report": "Mantenimiento Preventivo",
    "items": [{"item_id": 1, "quantity": 2}],
    "request_id": null
  }'
```

#### **2. Usando `request_id` en el body**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/router/orders/' \
  -H 'Content-Type: application/json' \
  -d '{
    "report": "Mantenimiento Preventivo",
    "items": [{"item_id": 1, "quantity": 2}],
    "request_id": "order-001"
  }'
```

### Ejemplo de uso (Paso a paso)

**Petición 1** - Primera llamada (crea la orden):
```bash
POST /router/orders/
Header: Idempotency-Key: xyz789
→ Respuesta: 201 Created, order_id: 1
```

**Petición 2** - Misma `Idempotency-Key` (retorna la MISMA orden):
```bash
POST /router/orders/
Header: Idempotency-Key: xyz789
→ Respuesta: 201 Created, order_id: 1 (SIN DUPLICAR)
```

**Petición 3** - Diferente `Idempotency-Key` (crea nueva orden):
```bash
POST /router/orders/
Header: Idempotency-Key: abc999
→ Respuesta: 201 Created, order_id: 2 (nueva orden)
```

### Implementación técnica

1. **Base de datos**: Tabla `idempotency_keys` almacena las claves con su orden asociada
2. **Validación**: Antes de crear, verifica si la clave ya existe
3. **Transacción atómica**: Si dos requests llegan simultáneamente, solo uno crea la orden
4. **Garantía**: `UNIQUE INDEX` en la BD evita duplicados a nivel de base de datos

**Ubicación del código**: [app/services/order_service.py](app/services/order_service.py)

## ☁️ Integración con AWS S3 (Simulada)

### Módulo s3_service.py

Implementa lógica de conexión a AWS S3 usando **boto3** con simulación de operaciones.

**Características:**
- ✅ Inicialización del cliente S3 con credenciales
- ✅ Simulación de upload de imágenes (sin archivos reales)
- ✅ Simulación de listación de imágenes
- ✅ Simulación de eliminación de archivos
- ✅ Validación de nombres y extensiones
- ✅ **Manejo completo de excepciones**:
  - `NoCredentialsError`: Credenciales de AWS no disponibles
  - `ClientError`: Errores de comunicación con AWS
  - `ValueError`: Validaciones fallidas
  - `PermissionError`: Acceso denegado al bucket

### Ejemplos de uso en Swagger

**1. Simular subida de imagen:**
```json
POST /router/s3/simulate-upload-image
{
  "image_name": "IMG001.jpg",
  "maintenance_id": 1
}

Respuesta:
{
  "status": "success",
  "s3_url": "s3://mi-bucket-simulado/maintenance/1/IMG001.jpg",
  "object_key": "maintenance/1/IMG001.jpg",
  "bucket": "mi-bucket-simulado"
}
```

**2. Listar imágenes simuladas:**
```
GET /router/s3/simulate-list-images/1

Respuesta:
{
  "status": "success",
  "bucket": "mi-bucket-simulado",
  "prefix": "maintenance/1/",
  "total_images": 3,
  "images": [
    "maintenance/1/IMG001.jpg",
    "maintenance/1/IMG002.jpg",
    "maintenance/1/IMG003.jpg"
  ]
}
```

**3. Obtener información del bucket:**
```
GET /router/s3/bucket-info

Respuesta:
{
  "status": "success",
  "bucket_name": "mi-bucket-simulado",
  "region": "us-east-1",
  "accessible": true
}
```

### Ubicación del código
- Servicio: [app/services/s3_service.py](app/services/s3_service.py)
- Endpoints: [app/routers/s3.py](app/routers/s3.py)

## 📁 Estructura del Proyecto

```
Maintenance_Service_API/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── api.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   └── session.py
│   ├── models/
│   │   ├── item.py
│   │   ├── category.py
│   │   ├── order.py
│   │   └── idempotency.py
  │   ├── routers/
  │   │   ├── items.py
  │   │   ├── categories.py
  │   │   ├── orders.py
  │   │   └── s3.py
│   ├── schemas/
│   │   ├── item.py
│   │   ├── category.py
│   │   └── order.py
│   ├── services/
│   │   ├── item_service.py
│   │   ├── category_service.py
│   │   ├── order_service.py
│   │   └── s3_service.py
│   ├── utils/
│   │   └── decorators.py
│   └── main.py
├── .gitignore
├── README.md
└── requirements.txt
```

