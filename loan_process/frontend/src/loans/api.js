import axios from 'axios';

const loanAPI = axios.create({
  baseURL: '/api/',
});

loanAPI.interceptors.request.use(config => {
  const token = localStorage.getItem('access');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default loanAPI;
