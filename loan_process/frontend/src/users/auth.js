import API from './api';

export const loginUser = async (credentials) => {
  const res = await API.post('/api/login/',credentials);
  const data = res.data;
  if (res.ok) {
    localStorage.setItem('access', data.access);
    localStorage.setItem('refresh', data.refresh);
  }
  return data;
};

export const logoutUser = () => {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
};
