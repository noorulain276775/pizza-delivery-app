import React, { memo } from 'react';
import PropTypes from 'prop-types';

const LoadingSpinner = memo(({ message = 'Loading...', size = 'medium' }) => {
  const sizeClass = `loading-spinner-${size}`;
  
  return (
    <div className="loading">
      <div className={`loading-spinner ${sizeClass}`}></div>
      {message && <p className="loading-message">{message}</p>}
    </div>
  );
});

LoadingSpinner.propTypes = {
  message: PropTypes.string,
  size: PropTypes.oneOf(['small', 'medium', 'large'])
};

LoadingSpinner.defaultProps = {
  message: 'Loading...',
  size: 'medium'
};

LoadingSpinner.displayName = 'LoadingSpinner';

export default LoadingSpinner;
