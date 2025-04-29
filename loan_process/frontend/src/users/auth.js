import API from './api';

/**
 * Logs in the user by sending credentials to the backend API.
 * Stores the access and refresh tokens in localStorage on success.
 * @param {Object} credentials - The user's login credentials (e.g., email and password).
 * @returns {Object} - An object containing success status, message, and optional data.
 */
export const loginUser = async (credentials) => {
  try {
    // Send a login request to the API
    const res = await API.post('/api/users/auth/login/', credentials);
    const { access, refresh } = res.data;

    if (access && refresh) {
      // Store tokens in localStorage
      localStorage.setItem('access', access);
      localStorage.setItem('refresh', refresh);

      return {
        success: true,
        message: 'Login successful.',
        data: res.data,
      };
    } else {
      throw new Error('Invalid response: Access or Refresh token missing.');
    }
  } catch (err) {
    // Log the error for debugging
    console.error('Login error:', err);

    // Handle different error scenarios
    const errorMessage =
      err.response?.data?.detail || // Server-side validation error
      err.message || // Generic error message
      'Login failed. Please check your credentials.';

    return {
      success: false,
      message: errorMessage,
    };
  }
};

/**
 * Logs out the user by clearing tokens from localStorage.
 * Optionally, you can redirect the user to the login page or perform other actions.
 */
export const logoutUser = () => {
  // Clear tokens from localStorage
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');

  // Optionally, redirect to the login page
  window.location.href = '/login';
};