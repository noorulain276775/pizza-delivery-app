import React, { memo } from 'react';
import PropTypes from 'prop-types';

const PizzaCard = memo(({ pizza, onAddToCart, onImageError }) => {
  const handleAddToCart = () => {
    onAddToCart(pizza);
  };

  const handleImageError = (e) => {
    if (onImageError) {
      onImageError(e, pizza);
    } else {
      // Default fallback image
      e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjBmMGYwIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlPC90ZXh0Pjwvc3ZnPg==';
    }
  };

  return (
    <div className="pizza-card">
      <img 
        src={`/${pizza.image}`} 
        alt={pizza.name} 
        className="pizza-image"
        onError={handleImageError}
      />
      <div className="pizza-info">
        <h3>{pizza.name}</h3>
        <p className="ingredients">{pizza.ingredients}</p>
        <p className="price">${pizza.price}</p>
        <button 
          onClick={handleAddToCart}
          className="add-button"
          aria-label={`Add ${pizza.name} to cart`}
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
});

PizzaCard.propTypes = {
  pizza: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    ingredients: PropTypes.string.isRequired,
    price: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    image: PropTypes.string.isRequired
  }).isRequired,
  onAddToCart: PropTypes.func.isRequired,
  onImageError: PropTypes.func
};

PizzaCard.defaultProps = {
  onImageError: null
};

PizzaCard.displayName = 'PizzaCard';

export default PizzaCard;
