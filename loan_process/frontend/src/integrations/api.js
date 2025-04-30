import axios from 'axios';
import { API_CONFIG, AUTH_CONFIG } from '../config';

const integrationsAPI = axios.create({
  baseURL: API_CONFIG.baseURL,
  headers: API_CONFIG.headers,
  timeout: API_CONFIG.timeout,
});

// Add a request interceptor to include the Authorization header if the token exists
integrationsAPI.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // Handle errors occurring during request setup
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle errors globally
integrationsAPI.interceptors.response.use(
  (response) => response,
  (error) => {
    // Log the error for debugging
    console.error('API response error:', error);

    // Check if the error is due to an expired or invalid token
    if (error.response && error.response.status === 401) {
      // Handle token expiration (logout the user and redirect to login)
      console.warn('Unauthorized. Token might be expired or invalid.');
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      window.location.href = AUTH_CONFIG.loginRedirectUrl;
    }

    // Pass the error to the caller
    return Promise.reject(error);
  }
);

export default integrationsAPI;
