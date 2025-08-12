@echo off
echo Starting Pizza Delivery App (Backend + Frontend)
echo.

echo Starting Backend API...
start "Backend API" cmd /k "cd backend && python run.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm start"

echo.
echo Both services are starting...
echo Backend will be available at: http://localhost:5000
echo Frontend will be available at: http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul
