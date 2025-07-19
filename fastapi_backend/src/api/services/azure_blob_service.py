"""
Azure Blob Service: Asynchronous handler for uploading files to Azure Blob Storage.

Defines the core logic for:
  - Establishing connection via environment-variable loaded config
  - Async upload of files/streams to a specified container
  - Error handling
"""

import aiofiles

from azure.storage.blob.aio import BlobServiceClient
from azure.core.exceptions import AzureError


class AzureBlobService:
    """
    Service class providing async upload functionality to Azure Blob Storage.
    
    Loads configuration from environment variables and exposes a clean async API.
    """

    def __init__(self, connection_string: str, container_name: str):
        self.connection_string = connection_string
        self.container_name = container_name
        self._blob_service_client = None

    async def get_blob_service_client(self):
        """Lazily create the BlobServiceClient (async-safe)."""
        if not self._blob_service_client:
            self._blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        return self._blob_service_client

    # PUBLIC_INTERFACE
    async def upload_fileobj_async(self, file_obj, blob_name: str) -> str:
        """
        Async upload a file-like object to Azure Blob Storage.

        Args:
            file_obj: file-like object opened for reading bytes.
            blob_name (str): The name to give the uploaded blob.

        Returns:
            The URL of the uploaded blob.
        Raises:
            AzureError: If upload fails.
        """
        blob_service_client = await self.get_blob_service_client()
        container_client = blob_service_client.get_container_client(self.container_name)
        try:
            await container_client.upload_blob(name=blob_name, data=file_obj, overwrite=True)
            blob_url = f"{container_client.url}/{blob_name}"
            return blob_url
        except AzureError:
            raise

    # PUBLIC_INTERFACE
    async def upload_local_file_async(self, local_path: str, blob_name: str) -> str:
        """
        Async upload an on-disk file to Azure Blob Storage.

        Args:
            local_path (str): Path to the file on disk.
            blob_name (str): Name for blob in Azure.

        Returns:
            str: Blob URL.
        """
        async with aiofiles.open(local_path, "rb") as f:
            data = await f.read()
        return await self.upload_fileobj_async(data, blob_name)
