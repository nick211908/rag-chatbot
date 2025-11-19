@echo off
setlocal

echo Starting deployment process...

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found!
    echo Please create a .env file with your configuration.
    exit /b 1
)

REM Build and start services
echo Building and starting services...
docker-compose up --build -d

echo Deployment completed!
echo Frontend is available at: http://localhost:5000
echo Backend API is available at: http://localhost:8000

pause