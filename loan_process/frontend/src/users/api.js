import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  headers: { 'Content-Type': 'application/json' },
});

// Function to refresh the access token
const refreshAccessToken = async () => {
  try {
    const refreshToken = localStorage.getItem('refresh'); // Get the refresh token
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await axios.post(`${API.defaults.baseURL}api/token/refresh/`, {
      refresh: refreshToken,
    });

    const { access } = response.data;
    localStorage.setItem('access', access); // Update the access token
    return access;
  } catch (error) {
    console.error('Failed to refresh token:', error);
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    throw error; // If token refresh fails, log the user out or redirect them
  }
};

// Attach access token if available and refresh token if expired
API.interceptors.request.use(
  async (config) => {
    let token = localStorage.getItem('access');

    if (token) {
      const tokenExpiry = JSON.parse(atob(token.split('.')[1])).exp * 1000; // Decode the token expiry time
      const currentTime = Date.now();

      if (currentTime >= tokenExpiry) {
        // Token has expired, attempt to refresh it
        token = await refreshAccessToken();
      }

      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Global error handling for responses
API.interceptors.response.use(
  (response) => response, // Pass through successful responses
  async (error) => {
    if (error.response && error.response.status === 401) {
      console.error('Unauthorized access - possible invalid token');
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      // Optionally, redirect the user to the login page here
    }
    return Promise.reject(error);
  }
);

export default API;