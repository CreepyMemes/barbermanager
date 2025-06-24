import { useEffect, useState, useCallback } from 'react';
import AuthContext from './AuthContext';
import LoadingSpinner from '@components/common/LoadingSpinner/LoadingSpinner';
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
   * Helper callback function to automaticaly get the user profile by trying all profile endpoints.
   */
  const fetchUserAndProfile = useCallback(async () => {
    setLoading(true);

    try {
      // Fetch user basic info
      const { me } = await authApi.getCurrentUser();
      setUser(me);
      setIsAuthenticated(true);

      // Fetch role-specific profile
      let profileData = null;
      if (me.role === 'ADMIN') {
        profileData = await getAdminProfile();
      } else if (me.role === 'BARBER') {
        profileData = await getBarberProfile();
      } else if (me.role === 'CLIENT') {
        profileData = await getClientProfile();
      }
      setProfile(profileData);
    } catch (error) {
      setUser(null);
      setProfile(null);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Hydrates user on mount, checks if token exists in storage, then fetches profile data
   */
  useEffect(() => {
    if (authApi.getAccessToken() && authApi.getRefreshToken()) {
      fetchUserAndProfile();
    } else {
      setUser(null);
      setProfile(null);
      setIsAuthenticated(false);
      setLoading(false);
    }
  }, [fetchUserAndProfile]);

  /**
   * Handles login and sets everything up in context.
   */
  const login = async function (credentials) {
    setLoading(true);

    try {
      await authApi.login(credentials);
      await fetchUserAndProfile();
    } catch (error) {
      setUser(null);
      setProfile(null);
      setIsAuthenticated(false);
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
      setUser(null);
      setProfile(null);
      setIsAuthenticated(false);
    } finally {
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
      {loading ? <LoadingSpinner /> : children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
