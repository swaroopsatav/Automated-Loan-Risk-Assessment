import axios from 'axios';

const scoreApi = axios.create({
  baseURL: '/api/',
});

scoreApi.interceptors.request.use(config => {
  const token = localStorage.getItem('access');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default scoreApi;
