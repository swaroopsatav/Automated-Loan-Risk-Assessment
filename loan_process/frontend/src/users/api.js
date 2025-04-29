import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/',
  headers: { 'Content-Type': 'application/json' },
});

// Function to refresh the access token
const refreshAccessToken = async () => {
  try {
    const refreshToken = localStorage.getItem('refresh'); // Get the refresh token
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    // Send a request to refresh the token
    const response = await API.post('api/token/refresh/', {
      refresh: refreshToken,
    });

    const { access } = response.data;
    localStorage.setItem('access', access); // Update the access token
    return access;
  } catch (error) {
    console.error('Failed to refresh token:', error);

    // Clean up tokens on failure
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');

    // Optionally, redirect the user to the login page here
    window.location.href = '/login'; // Redirect to login page
    throw error; // Re-throw the error for further handling
  }
};

// Attach an access token if available and refresh the token if expired
API.interceptors.request.use(
  async (config) => {
    try {
      let token = localStorage.getItem('access');

      if (token) {
        // Decode the token to check expiry
        const tokenPayload = JSON.parse(atob(token.split('.')[1])); // Decode the token payload
        const tokenExpiry = tokenPayload.exp * 1000; // Convert expiry to milliseconds
        const currentTime = Date.now();

        // Refresh the token if it has expired
        if (currentTime >= tokenExpiry) {
          token = await refreshAccessToken();
        }

        // Attach the token to the request headers
        config.headers.Authorization = `Bearer ${token}`;
      }

      return config;
    } catch (error) {
      console.error('Error attaching token to request:', error);
      return Promise.reject(error);
    }
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Global error handling for responses
API.interceptors.response.use(
  (response) => response, // Pass through successful responses
  (error) => {
    if (error.response && error.response.status === 401) {
      console.error('Unauthorized access - possible invalid token');

      // Clean up tokens and redirect to log in
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      window.location.href = '/login'; // Redirect to the login page
    }
    return Promise.reject(error);
  }
);

export default API;