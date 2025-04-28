import API from './api';

export const loginUser = async (credentials) => {
  try {
    const res = await API.post('/api/login/', credentials);
    const data = res.data;

    if (data.access && data.refresh) {
      // Store tokens in localStorage
      localStorage.setItem('access', data.access);
      localStorage.setItem('refresh', data.refresh);
      return { success: true, message: 'Login successful', data };
    } else {
      throw new Error('Invalid response: Access or Refresh token missing');
    }
  } catch (err) {
    console.error('Login error:', err.response?.data || err.message);
    return {
      success: false,
      message: err.response?.data?.detail || 'Login failed. Please check your credentials.',
    };
  }
};

export const logoutUser = () => {
  // Clear tokens from localStorage
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
};