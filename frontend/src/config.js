// Backend API configuration
export const API_CONFIG = {
  // Development: Backend running locally
  BASE_URL: process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000',
  
  // API endpoints
  ENDPOINTS: {
    PIZZAS: '/api/pizzas/',
    ORDERS: '/api/orders/',
    HEALTH: '/health'
  }
};

// Helper function to build full API URLs
export const buildApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};
