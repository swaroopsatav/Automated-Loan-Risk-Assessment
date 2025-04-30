// api.js
import axios from 'axios';
import { API_CONFIG, AUTH_CONFIG } from '../config';

const API = axios.create({
  baseURL: API_CONFIG.baseURL,
  headers: API_CONFIG.headers,
  timeout: API_CONFIG.timeout,
});

// Flag to prevent multiple refresh calls
let isRefreshing = false;

// Function to refresh the access token
const refreshAccessToken = async () => {
  try {
    const refreshToken = localStorage.getItem('refresh');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    // Call refresh endpoint
    const response = await API.post('/api/token/refresh/', {
      refresh: refreshToken,
    });

    const { access } = response.data;
    localStorage.setItem('access', access);
    return access;
  } catch (error) {
    console.error('Failed to refresh token:', error);

    // Clear tokens and redirect
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    window.location.href = AUTH_CONFIG.loginRedirectUrl;
    throw error;
  }
};

// Request interceptor: attach token and refresh if needed
API.interceptors.request.use(
  async (config) => {
    try {
      let token = localStorage.getItem('access');

      if (token) {
        const parts = token.split('.');
        if (parts.length !== 3) throw new Error('Invalid JWT structure');

        const payload = JSON.parse(atob(parts[1]));
        const tokenExpiry = payload.exp * 1000;
        const currentTime = Date.now();

        if (currentTime + AUTH_CONFIG.tokenExpiryBuffer >= tokenExpiry && !isRefreshing) {
          isRefreshing = true;
          token = await refreshAccessToken();
          isRefreshing = false;
        }

        config.headers.Authorization = `Bearer ${token}`;
      }

      return config;
    } catch (error) {
      console.error('Error attaching token to request:', error);
      return Promise.reject(error);
    }
  },
  (error) => Promise.reject(error)
);

// Response interceptor: handle global errors
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.warn('Unauthorized - redirecting to login');
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      window.location.href = AUTH_CONFIG.loginRedirectUrl;
    }
    return Promise.reject(error);
  }
);

export default API;
