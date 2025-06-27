import { useEffect, useState, useCallback } from 'react';
import AuthContext from '@contexts/AuthContext';
import api from '@api';

/**
 * This provides authentication info, user, profile, login/logout logic.
 */
function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(!!api.auth.getAccessToken());
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  /**
   * Helper callback function for unified reset + redirect
   */
  const handleLogout = useCallback(() => {
    api.auth.removeTokens();
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
      const { me } = await api.auth.getCurrentUser();
      setUser(me);
      setIsAuthenticated(true);

      // Fetch role specific profile
      if (me.role === 'ADMIN') {
        const { profile } = await api.admin.getAdminProfile();
        setProfile(profile);
      } else if (me.role === 'BARBER') {
        const { profile } = await api.barber.getBarberProfile();
        setProfile(profile);
      } else if (me.role === 'CLIENT') {
        const { profile } = await api.client.getClientProfile();
        setProfile(profile);
      }
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
    if (api.auth.getRefreshToken()) {
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
      await api.auth.login(credentials);
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
      await api.auth.logout();
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
