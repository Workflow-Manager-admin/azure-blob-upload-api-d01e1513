"""
Config Loader: Encapsulates loading configuration from environment variables using python-dotenv or os.environ.
"""

import os
from dotenv import load_dotenv

# Load .env at import time for all dependent modules (safe for FastAPI uvicorn reloads)
dotenv_loaded = load_dotenv()

class Settings:
    """
    App settings loaded from the environment.
    - AZURE_STORAGE_CONNECTION_STRING: Azure Blob Storage connection string
    - AZURE_STORAGE_CONTAINER_NAME: Target blob container name
    """
    AZURE_STORAGE_CONNECTION_STRING: str = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    AZURE_STORAGE_CONTAINER_NAME: str = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "uploads")

    def validate(self):
        if not self.AZURE_STORAGE_CONNECTION_STRING:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING is required in environment!")
        if not self.AZURE_STORAGE_CONTAINER_NAME:
            raise ValueError("AZURE_STORAGE_CONTAINER_NAME is required in environment!")

settings = Settings()
settings.validate()
