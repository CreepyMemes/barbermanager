import { useEffect, useState, useCallback } from 'react';
import AuthContext from '@contexts/AuthContext';

import * as authApi from '@api/authApi';

import { getAdminProfile } from '../api/services/adminService';
import { getBarberProfile } from '../api/services/barberService';
import { getClientProfile } from '../api/services/clientService';

/**
 * This provides authentication info, user, profile, login/logout logic.
 */
function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(!!authApi.getAccessToken());
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  /**
   * Helper callback function for unified reset + redirect
   */
  const handleLogout = useCallback(() => {
    authApi.removeTokens();
    setUser(null);
    setProfile(null);
    setIsAuthenticated(false);
  }, []);

  /**
   * Helper callback function to automaticaly get the user profile by trying all profile endpoints.
   */
  const fetchUserAndProfile = useCallback(async () => {
    setLoading(true);

    try {
      // Fetch user basic info
      const { me } = await authApi.getCurrentUser();
      setUser(me);
      setIsAuthenticated(true);

      // Fetch role specific profile
      let profileData = null;
      if (me.role === 'ADMIN') profileData = await getAdminProfile();
      else if (me.role === 'BARBER') profileData = await getBarberProfile();
      else if (me.role === 'CLIENT') profileData = await getClientProfile();

      setProfile(profileData);
    } catch {
      handleLogout();
    } finally {
      setLoading(false);
    }
  }, [handleLogout]);

  /**
   * Hydrates user on mount if tokens exists in storage
   */
  useEffect(() => {
    if (authApi.getRefreshToken()) {
      fetchUserAndProfile();
    } else {
      handleLogout();
      setLoading(false);
    }
  }, [fetchUserAndProfile, handleLogout]);

  /**
   * Handles login and sets everything up in context.
   */
  const login = async (credentials) => {
    setLoading(true);

    try {
      await authApi.login(credentials);
      await fetchUserAndProfile();
    } finally {
      setLoading(false);
    }
  };

  /**
   * Logout for manual invocation or on refresh error, clears tokens
   */
  const logout = async () => {
    setLoading(true);

    try {
      await authApi.logout();
    } finally {
      handleLogout();
      setLoading(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user, // from /auth/me/
        profile, // from profile endpoint, might be null or richer info
        loading, // true during login/profile-fetch
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
