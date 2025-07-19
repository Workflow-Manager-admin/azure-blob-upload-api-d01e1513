#!/bin/bash
cd /home/kavia/workspace/code-generation/azure-blob-upload-api-d01e1513/fastapi_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

