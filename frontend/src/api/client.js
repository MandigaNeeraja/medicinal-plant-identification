import axios from 'axios';

const API_ROOT = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL.replace(/\/$/, '')}/api`
  : '/api';

const TOKEN_KEY = 'access_token';

export function getAccessToken() {
  return sessionStorage.getItem(TOKEN_KEY);
}

export function setAccessToken(token) {
  if (token) {
    sessionStorage.setItem(TOKEN_KEY, token);
  } else {
    sessionStorage.removeItem(TOKEN_KEY);
  }
}

export function clearAccessToken() {
  sessionStorage.removeItem(TOKEN_KEY);
}

const api = axios.create({
  baseURL: API_ROOT,
  withCredentials: true,
});

let refreshPromise = null;

async function refreshAccessToken() {
  if (!refreshPromise) {
    refreshPromise = api.post('/auth/refresh').finally(() => {
      refreshPromise = null;
    });
  }
  const response = await refreshPromise;
  const token = response.data?.data?.access_token;
  if (token) {
    setAccessToken(token);
  }
  return response;
}

api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  // Let the browser set multipart boundary automatically
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type'];
  } else if (!config.headers['Content-Type']) {
    config.headers['Content-Type'] = 'application/json';
  }

  return config;
});

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
        clearAccessToken();
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
