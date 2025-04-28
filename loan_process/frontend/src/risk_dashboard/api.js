import axios from 'axios';

const riskAPI = axios.create({ baseURL: '/api/' });

riskAPI.interceptors.request.use(config => {
  const token = localStorage.getItem('access');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default riskAPI;
