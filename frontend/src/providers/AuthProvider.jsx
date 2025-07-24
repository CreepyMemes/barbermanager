import { useEffect, useState, useCallback } from 'react';
import AuthContext from '@contexts/AuthContext';
import api from '@api';
import { setGlobalLogout } from '@utils/globalLogout';

/**
 * This provides authentication info, user, profile, login/logout logic.
 */
function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(!!api.auth.getAccessToken());

  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);

  const [isFetchingProfile, setIsFetchingProfile] = useState(false);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

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
   * Assigns the global logout function reference whenever component is mounted (and cleanup on unmount)
   */
  useEffect(() => {
    setGlobalLogout(handleLogout);
    return () => setGlobalLogout(null);
  }, [handleLogout]);

  /**
   * Helper callback function to automaticaly get the user profile by trying all profile endpoints.
   */
  const fetchProfile = useCallback(async () => {
    setIsFetchingProfile(true);

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
    } catch (error) {
      console.error('Failed to fetch profile', error);
      handleLogout();
    } finally {
      setIsFetchingProfile(false);
    }
  }, [handleLogout]);

  /**
   * Hydrates user on mount if tokens exists in storage
   */
  useEffect(() => {
    if (api.auth.getRefreshToken()) {
      fetchProfile();
    } else {
      handleLogout();
    }
  }, [fetchProfile, handleLogout]);

  /**
   * Handles login and sets everything up in context.
   */
  const login = async (credentials) => {
    setIsLoggingIn(true);

    try {
      await api.auth.login(credentials); // Any exceptions get catched in the login Form
      await fetchProfile();
    } finally {
      setIsLoggingIn(false);
    }
  };

  /**
   * Logout for manual invocation or on refresh error, clears tokens
   */
  const logout = async () => {
    setIsLoggingOut(true);

    try {
      await api.auth.logout();
    } finally {
      handleLogout();
      setIsLoggingOut(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated, // True only when user is authenticated

        user, // basic user information (form api/auth/me)
        profile, // role based profie information (from /api/<role>/profile)
        isFetchingProfile, // passed to handle loading status
        setProfile, // to always set latest profile data

        isLoggingIn, // only true during login()
        login,

        isLoggingOut, // only true during logout()
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
