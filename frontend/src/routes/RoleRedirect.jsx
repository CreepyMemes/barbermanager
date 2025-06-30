import { useLocation, Navigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';

/**
 * Redirects only for shortcuts, from `/:page` to `/:role/:page`
 */
function RoleRedirect() {
  const { isAuthenticated, isFetchingProfile, profile } = useAuth();
  const location = useLocation();

  // Don't do anything if user is not authenticattd or still fetching user data
  if (!isAuthenticated || isFetchingProfile || !profile) return null;

  // Always in a known path (dashboard/settings/profile) at this point.
  const page = location.pathname.replace(/^\//, '');

  // Redirect `/:page` to `/:role/:page`
  return <Navigate to={`/${profile.role.toLowerCase()}/${page}`} replace />;
}

export default RoleRedirect;
