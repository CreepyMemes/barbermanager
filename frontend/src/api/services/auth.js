import axiosInstance from '@api/axiosInstance';
import { ENDPOINTS } from '@api/endpoints';

/**
 * Keys used for storing authentication tokens in localStorage.
 */
const STORAGE_KEYS = {
  ACCESS: 'access_token',
  REFRESH: 'refresh_token',
};

/**
 * Retrieves the access token from localStorage.
 */
export function getAccessToken() {
  return localStorage.getItem(STORAGE_KEYS.ACCESS);
}

/**
 * Retrieves the refresh token from localStorage.
 */
export function getRefreshToken() {
  return localStorage.getItem(STORAGE_KEYS.REFRESH);
}

/**
 * Stores the access and refresh tokens in localStorage.
 */
export function setTokens({ access, refresh }) {
  localStorage.setItem(STORAGE_KEYS.ACCESS, access);
  localStorage.setItem(STORAGE_KEYS.REFRESH, refresh);
}

/**
 * Removes the access and refresh tokens from localStorage.
 */
export function removeTokens() {
  localStorage.removeItem(STORAGE_KEYS.ACCESS);
  localStorage.removeItem(STORAGE_KEYS.REFRESH);
}

/**
 * Retrieves the current users's information.
 */
export async function getCurrentUser() {
  const { data } = await axiosInstance.get(ENDPOINTS.auth.me);
  return data;
}

/**
 * Logs in a user using email or username along with password.
 * Stores the received tokens in localStorage.
 */
export async function login({ email, username, password }) {
  const payload = { password };
  if (email) payload.email = email;
  if (username) payload.username = username;

  const { data } = await axiosInstance.post(ENDPOINTS.auth.login, payload);
  const { user, token } = data;

  setTokens({
    access: token.access_token,
    refresh: token.refresh_token,
  });

  return user; // return the user directly!
}

/**
 * Logs out the user by invalidating the refresh token on the server
 */
export async function logout() {
  const refresh = getRefreshToken();
  try {
    if (refresh) {
      await axiosInstance.post(ENDPOINTS.auth.logout, { refresh_token: refresh });
    }
  } catch (_) {
    // ignore API errors during logout
  }
  removeTokens();
}

/**
 * Refreshes the access token using the refresh token.
 */
export async function refreshToken() {
  const refresh = getRefreshToken();
  if (!refresh) throw new Error('No refresh token');

  const { data } = await axiosInstance.post(ENDPOINTS.auth.refresh, { refresh_token: refresh });

  localStorage.setItem(STORAGE_KEYS.ACCESS, data.access_token);

  return data;
}

/**
 * Registers a new client account.
 */
export async function registerClient(clientData) {
  const { data } = await axiosInstance.post(ENDPOINTS.auth.registerClient, clientData);
  return data;
}

/**
 * Registers a new barber account using a verification token and UID.
 */
export async function registerBarber(uidb64, token, barberData) {
  const { data } = await axiosInstance.post(ENDPOINTS.auth.registerBarber(uidb64, token), barberData);
  return data;
}

/**
 * Sends a password reset request to the provided email address.
 */
export async function requestPasswordReset(email) {
  const { data } = await axiosInstance.post(ENDPOINTS.auth.resetPassword, { email });
  return data;
}

/**
 * Confirms and applies a new password using the reset token and UID.
 */
export async function confirmPasswordReset(uidb64, token, password) {
  const { data } = await axiosInstance.post(ENDPOINTS.auth.resetPasswordConfirm(uidb64, token), { password });
  return data;
}

/**
 * Verifies the user's email using a UID and token.
 */
export async function verifyEmail(uidb64, token) {
  const { data } = await axiosInstance.get(ENDPOINTS.auth.verifyEmail(uidb64, token));
  return data;
}
