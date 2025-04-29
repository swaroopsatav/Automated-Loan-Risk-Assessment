import React from 'react';
import { Navigate } from 'react-router-dom';

/**
 * Validates the JWT token by checking its existence and expiry time.
 * @returns {boolean} - True if the token is valid, false otherwise.
 */
const isTokenValid = () => {
  const token = localStorage.getItem('access');
  if (!token) return false;

  try {
    // Decode JWT payload
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
    return payload.exp > currentTime; // Token is valid if expiry time is in the future
  } catch (error) {
    console.error('Invalid or malformed token:', error);
    return false; // Treat invalid tokens as expired
  }
};

const PrivateRoute = ({ children }) => {
  return isTokenValid() ? children : <Navigate to="/login" replace />;
};

export default PrivateRoute;