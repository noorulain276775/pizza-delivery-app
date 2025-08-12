import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { buildApiUrl, API_CONFIG } from '../config';

const usePizzas = () => {
  const [pizzas, setPizzas] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPizzas = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      console.log('Fetching pizzas from API...');
      
      const response = await axios.get(buildApiUrl(API_CONFIG.ENDPOINTS.PIZZAS));
      console.log('Pizzas received:', response.data);
      
      setPizzas(response.data);
    } catch (err) {
      console.error('Error fetching pizzas:', err);
      
      let errorMessage = 'Error loading pizzas';
      if (err.code === 'ECONNREFUSED') {
        errorMessage = `Cannot connect to backend API at ${API_CONFIG.BASE_URL}. Please ensure the backend is running.`;
      } else if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const refreshPizzas = useCallback(() => {
    fetchPizzas();
  }, [fetchPizzas]);

  const getPizzaById = useCallback((id) => {
    return pizzas.find(pizza => pizza.id === id);
  }, [pizzas]);

  const getPizzasByCategory = useCallback((category) => {
    return pizzas.filter(pizza => pizza.category === category);
  }, [pizzas]);

  // Fetch pizzas on mount
  useEffect(() => {
    fetchPizzas();
  }, [fetchPizzas]);

  return {
    // State
    pizzas,
    isLoading,
    error,
    
    // Actions
    fetchPizzas,
    refreshPizzas,
    
    // Utilities
    getPizzaById,
    getPizzasByCategory,
    
    // Computed values
    hasPizzas: pizzas.length > 0,
    pizzaCount: pizzas.length
  };
};

export default usePizzas;
