"""
API Router for File Upload: Handles HTTP API interactions for uploading files to Azure Blob Storage.

Organized as a FastAPI APIRouter with OpenAPI documentation.
- POST /upload/ endpoint for file upload (multipart/form-data)
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from azure.core.exceptions import AzureError

from ..config import settings
from ..services.azure_blob_service import AzureBlobService

router = APIRouter(
    prefix="/upload",
    tags=["File Upload"]
)

# Single instance of AzureBlobService for request reuse
azure_blob_service = AzureBlobService(
    settings.AZURE_STORAGE_CONNECTION_STRING,
    settings.AZURE_STORAGE_CONTAINER_NAME
)

# PUBLIC_INTERFACE
@router.post("/", summary="Upload a file to Azure Blob Storage", response_description="Blob URL",
             status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file to Azure Blob Storage asynchronously.

    - **file**: file to be uploaded (multipart)
    - Returns: JSON with blob_url if successful.
    """
    try:
        # Read the file bytes asynchronously
        file_bytes = await file.read()
        blob_url = await azure_blob_service.upload_fileobj_async(file_bytes, file.filename)
        return {"blob_url": blob_url}
    except AzureError as e:
        # Azure errors (connection, permission, etc)
        raise HTTPException(status_code=500, detail=f"Azure upload failed: {str(e)}")
    except Exception as e:
        # Unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
