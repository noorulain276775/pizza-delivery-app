# Frontend API Configuration

## Overview
The frontend is now configured to connect directly to the backend API using a configurable base URL instead of relying on proxy settings.

## Configuration

### Default Configuration
By default, the frontend connects to: `http://127.0.0.1:5000`

### Environment Variable Configuration
To change the backend URL, set the `REACT_APP_API_URL` environment variable:

**Windows:**
```cmd
set REACT_APP_API_URL=http://your-backend-ip:5000
npm start
```

**Unix/Linux/Mac:**
```bash
export REACT_APP_API_URL=http://your-backend-ip:5000
npm start
```

### Configuration File
The main configuration is in `src/config.js`:

```javascript
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000',
  ENDPOINTS: {
    PIZZAS: '/api/pizzas/',
    ORDERS: '/api/orders/',
    HEALTH: '/health'
  }
};
```

## Use Cases

### Development
- **Local Backend**: `http://127.0.0.1:5000` (default)
- **Remote Backend**: `http://192.168.1.100:5000`

### Production
- **Production Backend**: `https://api.yourdomain.com`
- **Staging Backend**: `https://staging-api.yourdomain.com`

## Benefits

1. **Flexible**: Easy to change backend URL for different environments
2. **Production Ready**: Can point to any IP/domain
3. **No Proxy Issues**: Direct connection to backend
4. **Clear Configuration**: All API settings in one place

## Testing

To test different backend URLs:

1. Stop the frontend (`Ctrl+C`)
2. Set the environment variable
3. Restart the frontend (`npm start`)
4. Check browser console for connection status

## Troubleshooting

- **Connection Refused**: Check if backend is running on the specified URL
- **CORS Errors**: Ensure backend CORS is configured for the frontend URL
- **404 Errors**: Verify the backend endpoints are accessible
