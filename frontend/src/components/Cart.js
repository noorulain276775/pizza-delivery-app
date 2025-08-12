import React, { memo } from 'react';
import PropTypes from 'prop-types';

const Cart = memo(({ 
  cart, 
  onUpdateQuantity, 
  onRemoveItem, 
  onClearCart,
  cartTotal,
  cartItemCount 
}) => {
  if (cart.length === 0) {
    return (
      <div className="cart-section">
        <h2>Your Order</h2>
        <p className="empty-cart">Your cart is empty. Add some pizzas!</p>
      </div>
    );
  }

  return (
    <div className="cart-section">
      <h2>Your Order</h2>
      
      <div className="cart-items">
        {cart.map(item => (
          <div key={item.pizza_id} className="cart-item">
            <div className="item-info">
              <span className="item-name">{item.pizza_name}</span>
              <span className="item-price">${item.price}</span>
            </div>
            <div className="quantity-controls">
              <button 
                onClick={() => onUpdateQuantity(item.pizza_id, item.quantity - 1)}
                className="quantity-btn"
                title="Decrease quantity"
                aria-label="Decrease quantity"
              >
                −
              </button>
              <span className="quantity">{item.quantity}</span>
              <button 
                onClick={() => onUpdateQuantity(item.pizza_id, item.quantity + 1)}
                className="quantity-btn"
                title="Increase quantity"
                aria-label="Increase quantity"
              >
                +
              </button>
            </div>
            <button 
              onClick={() => onRemoveItem(item.pizza_id)}
              className="remove-btn"
              title="Remove item from cart"
              aria-label="Remove item from cart"
            >
              Remove
            </button>
          </div>
        ))}
      </div>

      <div className="cart-total">
        <div className="total-label">Order Total</div>
        <div className="total-amount">${cartTotal}</div>
        <div className="total-items">{cartItemCount} items</div>
      </div>

      <div className="cart-actions">
        <button 
          onClick={onClearCart}
          className="clear-cart-btn"
          title="Clear all items from cart"
        >
          Clear Cart
        </button>
      </div>
    </div>
  );
});

Cart.propTypes = {
  cart: PropTypes.arrayOf(PropTypes.shape({
    pizza_id: PropTypes.number.isRequired,
    pizza_name: PropTypes.string.isRequired,
    price: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    quantity: PropTypes.number.isRequired
  })).isRequired,
  onUpdateQuantity: PropTypes.func.isRequired,
  onRemoveItem: PropTypes.func.isRequired,
  onClearCart: PropTypes.func.isRequired,
  cartTotal: PropTypes.string.isRequired,
  cartItemCount: PropTypes.number.isRequired
};

Cart.displayName = 'Cart';

export default Cart;
