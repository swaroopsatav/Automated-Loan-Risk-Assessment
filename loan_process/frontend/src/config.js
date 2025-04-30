// Configuration file for the application
// This file centralizes configuration settings for easier maintenance

// API configuration
export const API_CONFIG = {
  // Base URL for API requests
  baseURL: 'http://localhost:8000',
  
  // Default headers for API requests
  headers: { 
    'Content-Type': 'application/json' 
  },
  
  // Timeout in milliseconds for API requests
  timeout: 10000,
};

// Authentication configuration
export const AUTH_CONFIG = {
  // Token expiry buffer in milliseconds (30 seconds)
  tokenExpiryBuffer: 30 * 1000,
  
  // Login redirect URL
  loginRedirectUrl: '/login',
  
  // Profile page URL
  profileUrl: '/profile',
};