"""
Main FastAPI application entrypoint.

- Registers API routers
- Loads configuration
- Sets up CORS
- Configures project-level OpenAPI metadata
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the upload router
from .routes.upload import router as upload_router

app = FastAPI(
    title="Async File Upload API",
    description="FastAPI application for asynchronous file uploads to Azure Blob Storage, with modular architecture.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (add new routers here for scaling)
app.include_router(upload_router)

@app.get("/")
def health_check():
    """Health Check Endpoint: Returns app status."""
    return {"message": "Healthy"}
