import api from '@api';
import axiosInstance from './instance';
import { performGlobalLogout } from '@utils/globalLogout';

/**
 * Variable that tracks the current refresh promise
 */
let refreshPromise = null;

/**
 * Attach access token to every request
 */
axiosInstance.interceptors.request.use(
  (config) => {
    const token = api.auth.getAccessToken();
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error),
);

/**
 * Handles 401 errors, attempts to refresh the token if found
 */
axiosInstance.interceptors.response.use(
  (response) => response,

  async (error) => {
    const original = error.config;

    // Don't process if not 401 or already retried
    if (error.response?.status !== 401 || original._retry) {
      return Promise.reject(error);
    }

    // Remove everything and bubble up for logout if no refresh token found
    if (!api.auth.getRefreshToken()) {
      api.auth.removeTokens();
      performGlobalLogout();
      return Promise.reject(error); // just throw, AuthProvider will handle redirect
    }

    original._retry = true;

    // Ensure only one refresh request at a time
    if (!refreshPromise) {
      refreshPromise = api.auth
        .refreshToken()
        .catch((error) => {
          api.auth.removeTokens();
          throw error;
        })
        .finally(() => {
          refreshPromise = null;
        });
    }

    // Wait for refresh, then retry
    try {
      const newAccess = await refreshPromise;
      original.headers.Authorization = `Bearer ${newAccess}`;
      return axiosInstance(original);
    } catch (error) {
      return Promise.reject(error);
    }
  },
);

export default axiosInstance;
