#!/bin/bash

echo "Starting Pizza Delivery App (Backend + Frontend)"
echo

echo "Starting Backend API..."
cd backend
python run.py &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 5

echo "Starting Frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo
echo "Both services are starting..."
echo "Backend will be available at: http://localhost:5000"
echo "Frontend will be available at: http://localhost:3000"
echo
echo "Press Ctrl+C to stop both services"

# Wait for user to stop
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
