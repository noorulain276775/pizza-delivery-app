import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import { buildApiUrl, API_CONFIG } from './config';

function App() {
  const [pizzas, setPizzas] = useState([]);
  const [cart, setCart] = useState([]);
  const [customerName, setCustomerName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [isOrdering, setIsOrdering] = useState(false);
  const [orderMessage, setOrderMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [cartTotal, setCartTotal] = useState(0);

  useEffect(() => {
    fetchPizzas();
  }, []);

  const fetchPizzas = async () => {
    try {
      setIsLoading(true);
      console.log('Fetching pizzas from API...');
      const response = await axios.get(buildApiUrl(API_CONFIG.ENDPOINTS.PIZZAS));
      console.log('Pizzas received:', response.data);
      setPizzas(response.data);
      setOrderMessage('');
    } catch (error) {
      console.error('Error fetching pizzas:', error);
      if (error.code === 'ECONNREFUSED') {
        setOrderMessage(`Cannot connect to backend API at ${API_CONFIG.BASE_URL}. Please ensure the backend is running.`);
      } else {
        setOrderMessage(`Error loading pizzas: ${error.message}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const addToCart = (pizza) => {
    const existingItem = cart.find(item => item.pizza_id === pizza.id);
    if (existingItem) {
      setCart(cart.map(item => 
        item.pizza_id === pizza.id 
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, { pizza_id: pizza.id, pizza_name: pizza.name, price: pizza.price, quantity: 1 }]);
    }
    
    // Smooth scroll to order section
    setTimeout(() => {
      document.querySelector('.order-section').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
    }, 300);
  };

  const removeFromCart = (pizzaId) => {
    setCart(cart.filter(item => item.pizza_id !== pizzaId));
  };

  const updateQuantity = (pizzaId, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromCart(pizzaId);
    } else {
      setCart(cart.map(item => 
        item.pizza_id === pizzaId 
          ? { ...item, quantity: newQuantity }
          : item
      ));
    }
  };

  const getTotalPrice = () => {
    return cart.reduce((total, item) => total + (parseFloat(item.price) * item.quantity), 0).toFixed(2);
  };

  // Update cart total whenever cart changes
  useEffect(() => {
    setCartTotal(parseFloat(getTotalPrice()));
  }, [cart]);

  const handleSubmitOrder = async (e) => {
    e.preventDefault();
          if (!customerName.trim() || !phoneNumber.trim()) {
                 setOrderMessage('Please fill in all fields');
         return;
       }
       if (cart.length === 0) {
         setOrderMessage('Please add items to your cart');
         return;
       }

    setIsOrdering(true);
    setOrderMessage('');

    try {
      const orderData = {
        customer_name: customerName.trim(),
        phone_number: phoneNumber.trim(),
        items: cart.map(item => ({
          pizza_id: item.pizza_id,
          quantity: item.quantity
        }))
      };

      console.log('Submitting order:', orderData);
      const response = await axios.post(buildApiUrl(API_CONFIG.ENDPOINTS.ORDERS), orderData);
      console.log('Order response:', response.data);
      
             setOrderMessage(`Order placed successfully! Order ID: ${response.data.id}. Total: $${response.data.total_price}. Cash on delivery.`);
      setCart([]);
      setCustomerName('');
      setPhoneNumber('');
    } catch (error) {
      console.error('Order submission error:', error);
      if (error.code === 'ECONNREFUSED') {
        setOrderMessage(`Cannot connect to backend API at ${API_CONFIG.BASE_URL}. Please ensure the backend is running.`);
      } else if (error.response?.data?.error) {
        setOrderMessage(`Order failed: ${error.response.data.error}`);
      } else if (error.response?.data?.details) {
        setOrderMessage(`Order failed: ${error.response.data.error}. Details: ${JSON.stringify(error.response.data.details)}`);
      } else {
        setOrderMessage(`Order failed: ${error.message || 'Please try again.'}`);
      }
    } finally {
      setIsOrdering(false);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>Pizza Delivery</h1>
        <p>Order delicious pizzas with cash on delivery</p>
        <div className="header-stats">
          <span className="stat-item">Easy Ordering</span>
          <span className="stat-item">Fast Delivery</span>
          <span className="stat-item">Cash on Delivery</span>
          {cart.length > 0 && (
            <span className="stat-item cart-count">{cart.reduce((sum, item) => sum + item.quantity, 0)} Items</span>
          )}
        </div>
      </header>

      <div className="container">
        <div className="pizza-section">
          <h2>Available Pizzas</h2>
          {isLoading ? (
            <div className="loading">
              <div className="loading-spinner"></div>
              <p>Loading delicious pizzas...</p>
            </div>
          ) : (
            <div className="pizza-grid">
              {pizzas.map(pizza => (
              <div key={pizza.id} className="pizza-card">
                <img 
                  src={`/${pizza.image}`} 
                  alt={pizza.name} 
                  className="pizza-image"
                  onError={(e) => {
                    console.error(`Failed to load image: ${pizza.image}`);
                    e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjBmMGYwIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlPC90ZXh0Pjwvc3ZnPg==';
                  }}
                />
                <div className="pizza-info">
                  <h3>{pizza.name}</h3>
                  <p className="ingredients">{pizza.ingredients}</p>
                  <p className="price">${pizza.price}</p>
                  <button 
                    onClick={() => addToCart(pizza)}
                    className="add-button"
                  >
                                         Add to Cart
                  </button>
                </div>
                              </div>
              ))}
            </div>
          )}
        </div>

        <div className="order-section">
          <h2>Your Order</h2>
          
          {cart.length === 0 ? (
            <p className="empty-cart">Your cart is empty. Add some pizzas!</p>
          ) : (
            <>
              <div className="cart-items">
                {cart.map(item => (
                  <div key={item.pizza_id} className="cart-item">
                    <div className="item-info">
                      <span className="item-name">{item.pizza_name}</span>
                      <span className="item-price">${item.price}</span>
                    </div>
                    <div className="quantity-controls">
                      <button 
                        onClick={() => updateQuantity(item.pizza_id, item.quantity - 1)}
                        className="quantity-btn"
                        title="Decrease quantity"
                      >
                        −
                      </button>
                      <span className="quantity">{item.quantity}</span>
                      <button 
                        onClick={() => updateQuantity(item.pizza_id, item.quantity + 1)}
                        className="quantity-btn"
                        title="Increase quantity"
                      >
                        +
                      </button>
                    </div>
                    <button 
                      onClick={() => removeFromCart(item.pizza_id)}
                      className="remove-btn"
                      title="Remove item from cart"
                    >
                                             Remove
                    </button>
                  </div>
                ))}
              </div>

              <div className="cart-total">
                <div className="total-label">Order Total</div>
                <div className="total-amount">${getTotalPrice()}</div>
                <div className="total-items">{cart.reduce((sum, item) => sum + item.quantity, 0)} items</div>
              </div>

              <form onSubmit={handleSubmitOrder} className="order-form">
                                 <h3>Delivery Information</h3>
                <div className="form-group">
                  <label htmlFor="customerName">Full Name:</label>
                  <input
                    type="text"
                    id="customerName"
                    value={customerName}
                    onChange={(e) => setCustomerName(e.target.value)}
                    placeholder="Enter your full name"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="phoneNumber">Phone Number:</label>
                  <input
                    type="tel"
                    id="phoneNumber"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    placeholder="+1234567890"
                    required
                  />
                </div>

                <div className="payment-info">
                  <p><strong>Payment Method:</strong> Cash on Delivery</p>
                </div>

                <button 
                  type="submit" 
                  className="order-button"
                  disabled={isOrdering}
                >
                  {isOrdering ? 'Placing Order...' : 'Place Order'}
                </button>
              </form>
            </>
          )}

          {orderMessage && (
            <div className={`message ${orderMessage.includes('successfully') ? 'success' : 'error'}`}>
              {orderMessage}
            </div>
          )}
        </div>
      </div>
      
             {/* Floating Cart Button */}
       {cart.length > 0 && (
         <div className="floating-cart" onClick={() => document.querySelector('.order-section').scrollIntoView({ behavior: 'smooth' })}>
           <div className="cart-badge">{cart.reduce((sum, item) => sum + item.quantity, 0)}</div>
           <span>View Cart</span>
         </div>
       )}
    </div>
  );
}

export default App;
