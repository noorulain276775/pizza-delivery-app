import React, { memo, useState } from 'react';
import PropTypes from 'prop-types';

const OrderForm = memo(({ onSubmit, isOrdering, cartItemCount }) => {
  const [customerName, setCustomerName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!customerName.trim() || !phoneNumber.trim()) {
      return;
    }

    onSubmit({
      customer_name: customerName.trim(),
      phone_number: phoneNumber.trim()
    });
  };

  const handleSuccess = () => {
    setCustomerName('');
    setPhoneNumber('');
  };

  const handleSubmitWithSuccess = (orderData) => {
    onSubmit(orderData, handleSuccess);
  };

  return (
    <form onSubmit={handleSubmit} className="order-form">
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
          disabled={isOrdering}
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
          disabled={isOrdering}
        />
      </div>

      <div className="payment-info">
        <p><strong>Payment Method:</strong> Cash on Delivery</p>
        <p><strong>Items in Cart:</strong> {cartItemCount}</p>
      </div>

      <button 
        type="submit" 
        className="order-button"
        disabled={isOrdering || cartItemCount === 0}
      >
        {isOrdering ? 'Placing Order...' : 'Place Order'}
      </button>
    </form>
  );
});

OrderForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  isOrdering: PropTypes.bool.isRequired,
  cartItemCount: PropTypes.number.isRequired
};

OrderForm.displayName = 'OrderForm';

export default OrderForm;
