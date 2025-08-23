#!/bin/bash
echo "Building and starting services..."
docker-compose up -d --build
echo "Services started. API is available at http://localhost:8000"