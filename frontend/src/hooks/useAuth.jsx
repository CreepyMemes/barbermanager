import { useContext } from 'react';
import AuthContext from '@contexts/AuthContext';

/**
 * Custom React hook for accessing authentication state and methods.
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
