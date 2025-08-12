import { useState, useCallback } from 'react';
import axios from 'axios';
import { buildApiUrl, API_CONFIG } from '../config';

const useOrder = () => {
  const [isOrdering, setIsOrdering] = useState(false);
  const [orderMessage, setOrderMessage] = useState('');
  const [lastOrder, setLastOrder] = useState(null);

  const submitOrder = useCallback(async (orderData, onSuccess) => {
    if (!orderData.customer_name?.trim() || !orderData.phone_number?.trim()) {
      setOrderMessage('Please fill in all fields');
      return { success: false, error: 'Please fill in all fields' };
    }

    if (!orderData.items || orderData.items.length === 0) {
      setOrderMessage('Please add items to your cart');
      return { success: false, error: 'Please add items to your cart' };
    }

    setIsOrdering(true);
    setOrderMessage('');

    try {
      console.log('Submitting order:', orderData);
      
      const response = await axios.post(buildApiUrl(API_CONFIG.ENDPOINTS.ORDERS), {
        customer_name: orderData.customer_name.trim(),
        phone_number: orderData.phone_number.trim(),
        items: orderData.items
      });
      
      console.log('Order response:', response.data);
      
      const successMessage = `Order placed successfully! Order ID: ${response.data.id}. Total: $${response.data.total_price}. Cash on delivery.`;
      setOrderMessage(successMessage);
      setLastOrder(response.data);
      
      // Call success callback if provided
      if (onSuccess && typeof onSuccess === 'function') {
        onSuccess(response.data);
      }
      
      return { success: true, data: response.data };
      
    } catch (err) {
      console.error('Order submission error:', err);
      
      let errorMessage = 'Order failed';
      if (err.code === 'ECONNREFUSED') {
        errorMessage = `Cannot connect to backend API at ${API_CONFIG.BASE_URL}. Please ensure the backend is running.`;
      } else if (err.response?.data?.error) {
        errorMessage = `Order failed: ${err.response.data.error}`;
      } else if (err.response?.data?.details) {
        errorMessage = `Order failed: ${err.response.data.error}. Details: ${JSON.stringify(err.response.data.details)}`;
      } else if (err.message) {
        errorMessage = `Order failed: ${err.message}`;
      } else {
        errorMessage = 'Order failed. Please try again.';
      }
      
      setOrderMessage(errorMessage);
      return { success: false, error: errorMessage };
      
    } finally {
      setIsOrdering(false);
    }
  }, []);

  const clearOrderMessage = useCallback(() => {
    setOrderMessage('');
  }, []);

  const resetOrder = useCallback(() => {
    setOrderMessage('');
    setLastOrder(null);
  }, []);

  return {
    // State
    isOrdering,
    orderMessage,
    lastOrder,
    
    // Actions
    submitOrder,
    clearOrderMessage,
    resetOrder,
    
    // Computed values
    hasOrderMessage: !!orderMessage,
    isSuccessMessage: orderMessage.includes('successfully'),
    isErrorMessage: orderMessage.includes('failed') || orderMessage.includes('Error')
  };
};

export default useOrder;
