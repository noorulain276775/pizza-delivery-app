import React, { useCallback } from 'react';
import { useCart, usePizzas, useOrder } from '../hooks';
import { PizzaCard, Cart, OrderForm, LoadingSpinner } from './index';

const Homepage = () => {
  // Custom hooks for state management
  const { 
    pizzas, 
    isLoading, 
    error, 
    hasPizzas 
  } = usePizzas();
  
  const { 
    cart, 
    cartTotal, 
    cartItemCount, 
    isCartEmpty,
    addToCart, 
    removeFromCart, 
    updateQuantity, 
    clearCart 
  } = useCart();
  
  const { 
    isOrdering, 
    orderMessage, 
    submitOrder, 
    clearOrderMessage 
  } = useOrder();

  // Handlers
  const handleAddToCart = useCallback((pizza) => {
    addToCart(pizza);
    
    // Smooth scroll to order section
    setTimeout(() => {
      document.querySelector('.order-section').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
    }, 300);
  }, [addToCart]);

  const handleSubmitOrder = useCallback((customerData) => {
    const orderData = {
      ...customerData,
      items: cart.map(item => ({
        pizza_id: item.pizza_id,
        quantity: item.quantity
      }))
    };

    submitOrder(orderData, () => {
      // Success callback - clear cart
      clearCart();
    });
  }, [cart, submitOrder, clearCart]);

  const scrollToCart = useCallback(() => {
    document.querySelector('.order-section').scrollIntoView({ behavior: 'smooth' });
  }, []);

  const handleImageError = useCallback((e, pizza) => {
    console.error(`Failed to load image: ${pizza.image}`);
    e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjBmMGYwIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlPC90ZXh0Pjwvc3ZnPg==';
  }, []);

  return (
    <>
      <header className="header">
        <h1>Pizza Delivery</h1>
        <p>Order delicious pizzas with cash on delivery</p>
        <div className="header-stats">
          <span className="stat-item">Easy Ordering</span>
          <span className="stat-item">Fast Delivery</span>
          <span className="stat-item">Cash on Delivery</span>
          {!isCartEmpty && (
            <span className="stat-item cart-count">
              {cartItemCount} Items
            </span>
          )}
        </div>
      </header>

      <div className="container">
        <div className="pizza-section">
          <h2>Available Pizzas</h2>
          
          {isLoading ? (
            <LoadingSpinner message="Loading delicious pizzas..." />
          ) : error ? (
            <div className="error-message">
              <p>{error}</p>
              <button onClick={() => window.location.reload()} className="retry-button">
                Retry
              </button>
            </div>
          ) : hasPizzas ? (
            <div className="pizza-grid">
              {pizzas.map(pizza => (
                <PizzaCard
                  key={pizza.id}
                  pizza={pizza}
                  onAddToCart={handleAddToCart}
                  onImageError={handleImageError}
                />
              ))}
            </div>
          ) : (
            <p className="no-pizzas">No pizzas available at the moment.</p>
          )}
        </div>

        <div className="order-section">
          <Cart
            cart={cart}
            onUpdateQuantity={updateQuantity}
            onRemoveItem={removeFromCart}
            onClearCart={clearCart}
            cartTotal={cartTotal}
            cartItemCount={cartItemCount}
          />

          {!isCartEmpty && (
            <OrderForm
              onSubmit={handleSubmitOrder}
              isOrdering={isOrdering}
              cartItemCount={cartItemCount}
            />
          )}

          {orderMessage && (
            <div className={`message ${orderMessage.includes('successfully') ? 'success' : 'error'}`}>
              {orderMessage}
              <button 
                onClick={clearOrderMessage}
                className="close-message-btn"
                aria-label="Close message"
              >
                ×
              </button>
            </div>
          )}
        </div>
      </div>
      
      {/* Floating Cart Button */}
      {!isCartEmpty && (
        <div className="floating-cart" onClick={scrollToCart}>
          <div className="cart-badge">{cartItemCount}</div>
          <span>View Cart</span>
        </div>
      )}
    </>
  );
};

export default Homepage;
