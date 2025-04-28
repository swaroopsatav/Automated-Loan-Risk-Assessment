import React from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('access');

  // Improved validation: Check if the token exists and is not expired
  const isTokenValid = () => {
    if (!token) return false;

    try {
      const payload = JSON.parse(atob(token.split('.')[1])); // Decode JWT payload
      const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
      return payload.exp > currentTime; // Token is valid if expiry time is in the future
    } catch (error) {
      console.error('Invalid token:', error);
      return false; // Treat invalid tokens as expired
    }
  };

  return isTokenValid() ? children : <Navigate to="/login" />;
};

export default PrivateRoute;