import axios from 'axios';
import { getAccessToken, getRefreshToken, refreshToken, removeTokens } from './authApi';

/**
 * Axios instance configured with base API URL and default headers.
 */
const axiosInstance = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

let isRefreshing = false;
let subscribers = [];

/**
 * Notify all subscribers with the new token.
 */
const notifySubscribers = (token) => {
  subscribers.forEach((callback) => callback(token));
  subscribers = [];
};

/**
 * Add a subscriber callback to be called once token is refreshed.
 */
const subscribeToRefresh = (callback) => {
  subscribers.push(callback);
};

/**
 * Attach access token to request headers.
 */
axiosInstance.interceptors.request.use(
  (config) => {
    const token = getAccessToken();
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error),
);

/**
 * Handles 401 errors: attempts to refresh the token or logs the user out.
 */
axiosInstance.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    // Don't process if not 401 or already retried
    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error);
    }

    // No refresh token - log out, stop, do not retry endlessly.
    if (!getRefreshToken()) {
      removeTokens();
      window.location.href = '/login';
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    if (!isRefreshing) {
      isRefreshing = true;
      try {
        const newToken = await refreshToken();
        isRefreshing = false;
        notifySubscribers(newToken);
      } catch (err) {
        isRefreshing = false;
        removeTokens();
        window.location.href = '/login';
        return Promise.reject(err);
      }
    }

    // Wait for refresh, then retry
    return new Promise((resolve) => {
      subscribeToRefresh((newToken) => {
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        resolve(axiosInstance(originalRequest));
      });
    });
  },
);

export default axiosInstance;
