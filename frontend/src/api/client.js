import axios from 'axios';

const API_ROOT = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL.replace(/\/$/, '')}/api`
  : '/api';

const api = axios.create({
  baseURL: API_ROOT,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

let refreshPromise = null;

async function refreshAccessToken() {
  if (!refreshPromise) {
    refreshPromise = api.post('/auth/refresh').finally(() => {
      refreshPromise = null;
    });
  }
  return refreshPromise;
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const status = error.response?.status;
    const isRefreshCall = originalRequest?.url?.includes('/auth/refresh');
    const isAuthCall = originalRequest?.url?.includes('/auth/login')
      || originalRequest?.url?.includes('/auth/register');

    if (status === 401 && !originalRequest._retry && !isRefreshCall && !isAuthCall) {
      originalRequest._retry = true;
      try {
        await refreshAccessToken();
        return api(originalRequest);
      } catch {
        if (!window.location.pathname.startsWith('/login')) {
          window.location.href = '/login';
        }
      }
    }

    return Promise.reject(error);
  },
);

export default api;

export function getErrorMessage(error) {
  return error.response?.data?.error || error.message || 'Something went wrong';
}
