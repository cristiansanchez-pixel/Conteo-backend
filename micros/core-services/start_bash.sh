#!/bin/bash

echo "🚀 Iniciando backend con Uvicorn..."
uvicorn app.main:app --reload --port 9007
