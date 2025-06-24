import { createContext, useEffect, useState, useCallback } from 'react';
import LoadingSpinner from '@components/common/LoadingSpinner/LoadingSpinner';
import * as authApi from '../api/authApi';
import { getAdminProfile } from '../api/services/adminService';
import { getBarberProfile } from '../api/services/barberService';
import { getClientProfile } from '../api/services/clientService';

/**
 * AuthContext setup
 */
const AuthContext = createContext(null);

/**
 * This provides authentication info, user, profile, login/logout logic.
 */
export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(!!authApi.getAccessToken());
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  /**
   * Helper callback function to automaticaly get the user profile by trying all profile endpoints.
   */
  const getUserProfile = useCallback(async () => {
    setLoading(true);
    try {
      const profileCallers = [getAdminProfile, getBarberProfile, getClientProfile];

      for (let caller of profileCallers) {
        try {
          const profile = await caller();
          setProfile(profile);
          setIsAuthenticated(true);
          return;
        } catch (_) {
          // Ignore and try the next one
        }
      }

      // All failed
      setProfile(null);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  }, []);

  // Hydrates user on mount, checks if token exists in storage, then fetches profile data
  useEffect(() => {
    if (authApi.getAccessToken()) {
      getUserProfile();
    } else {
      setLoading(false);
    }
  }, [getUserProfile]);

  /**
   * Handles login and sets everything up in context.
   */
  const login = async function (credentials) {
    setLoading(true);

    try {
      await authApi.login(credentials);
      await getUserProfile();
    } catch (_) {
      setIsAuthenticated(false);
      setProfile(null);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Logout logic, clears tokens and context state.
   */
  const logout = async function () {
    setLoading(true);
    try {
      await authApi.logout();
      setIsAuthenticated(false);
      setProfile(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        profile, // profile object or null
        loading, // true during login/profile-fetch
        login,
        logout,
      }}
    >
      {loading ? <LoadingSpinner /> : children}
    </AuthContext.Provider>
  );
}
