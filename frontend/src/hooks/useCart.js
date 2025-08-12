import { useState, useCallback, useMemo } from 'react';

const useCart = () => {
  const [cart, setCart] = useState([]);

  // Memoized cart calculations
  const cartTotal = useMemo(() => {
    return cart.reduce((total, item) => total + (parseFloat(item.price) * item.quantity), 0).toFixed(2);
  }, [cart]);

  const cartItemCount = useMemo(() => {
    return cart.reduce((sum, item) => sum + item.quantity, 0);
  }, [cart]);

  const isCartEmpty = useMemo(() => cart.length === 0, [cart]);

  // Cart actions
  const addToCart = useCallback((pizza) => {
    setCart(prevCart => {
      const existingItem = prevCart.find(item => item.pizza_id === pizza.id);
      if (existingItem) {
        return prevCart.map(item => 
          item.pizza_id === pizza.id 
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      } else {
        return [...prevCart, { 
          pizza_id: pizza.id, 
          pizza_name: pizza.name, 
          price: pizza.price, 
          quantity: 1 
        }];
      }
    });
  }, []);

  const removeFromCart = useCallback((pizzaId) => {
    setCart(prevCart => prevCart.filter(item => item.pizza_id !== pizzaId));
  }, []);

  const updateQuantity = useCallback((pizzaId, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromCart(pizzaId);
    } else {
      setCart(prevCart => prevCart.map(item => 
        item.pizza_id === pizzaId 
          ? { ...item, quantity: newQuantity }
          : item
      ));
    }
  }, [removeFromCart]);

  const clearCart = useCallback(() => {
    setCart([]);
  }, []);

  const getCartItem = useCallback((pizzaId) => {
    return cart.find(item => item.pizza_id === pizzaId);
  }, [cart]);

  return {
    // State
    cart,
    cartTotal,
    cartItemCount,
    isCartEmpty,
    
    // Actions
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    getCartItem,
    
    // Utility
    setCart
  };
};

export default useCart;
