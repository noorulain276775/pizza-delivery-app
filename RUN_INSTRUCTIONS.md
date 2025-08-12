# How to Run Pizza Delivery App

## Prerequisites
- Python 3.8+ with virtual environment activated
- Node.js 16+ and npm
- Backend dependencies installed
- Frontend dependencies installed

## Quick Start (Windows)
1. Double-click `run_both.bat`
2. This will open two command windows:
   - Backend API on http://localhost:5000
   - Frontend on http://localhost:3000

## Quick Start (Unix/Linux/Mac)
1. Make the script executable: `chmod +x run_both.sh`
2. Run: `./run_both.sh`
3. Both services will start automatically

## Manual Start

### Start Backend First
```bash
cd backend
python run.py
```
Backend will start on http://localhost:5000

### Start Frontend (in new terminal)
```bash
cd frontend
npm start
```
Frontend will start on http://localhost:3000

## Verify Everything is Working

1. **Backend Health Check**: Visit http://localhost:5000/health
   - Should show: `{"status": "healthy", "service": "pizza-delivery-api"}`

2. **Frontend**: Visit http://localhost:3000
   - Should display pizza menu
   - If no pizzas show, check browser console for errors

3. **API Endpoints**:
   - GET http://localhost:5000/api/pizzas/ - List all pizzas
   - POST http://localhost:5000/api/orders/ - Create order

## Troubleshooting

### Frontend shows "Cannot connect to backend API"
- Ensure backend is running on port 5000
- Check if port 5000 is not blocked by firewall
- Verify backend started without errors

### No pizzas displayed
- Check browser console for errors
- Verify backend has pizza data (run seed script if needed)
- Check if CORS is properly configured

### Port already in use
- Change port in backend/config.py or use different port
- Kill existing processes using the port

## Database Setup
If you need to populate the database with sample pizzas:
```bash
cd backend
python seed_data.py
```

## Stopping Services
- **Windows**: Close the command windows or press Ctrl+C
- **Unix/Linux**: Press Ctrl+C in the terminal running the script
