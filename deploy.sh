#!/bin/bash

# Exit on any error
set -e

echo "Starting deployment process..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create a .env file with your configuration."
    exit 1
fi

# Build and start services
echo "Building and starting services..."
docker-compose up --build -d

echo "Deployment completed!"
echo "Frontend is available at: http://localhost:5000"
echo "Backend API is available at: http://localhost:8000"