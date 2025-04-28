import axios from 'axios';

const complianceAPI = axios.create({ baseURL: '/api/' });

complianceAPI.interceptors.request.use(config => {
  const token = localStorage.getItem('access');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default complianceAPI;
