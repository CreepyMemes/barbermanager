import { Navigate, useParams } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';

import NotFound from '@pages/NotFound/NotFound';

/**
 * Blocks non authenticated users, (optionally) wrong role users
 * If routed with a :role param, redirect to canonical path if not matching.
 */
function ProtectedRoute({ children, role }) {
  const { isAuthenticated, isFetchingProfile, user } = useAuth();
  const { role: urlRole } = useParams();

  // Redirect to login if not authenticated
  if (!isAuthenticated) return <Navigate to="/login" replace />;

  // For static required role (e.g. /admin/barbers), show 404 if wrong role
  if (role && !isFetchingProfile && user && user.role !== role) {
    return <NotFound />;
  }

  // For dynamic :role routes, redirect to correct role path if role in URL doesn't match real role
  if (urlRole && !isFetchingProfile && user && urlRole.toLowerCase() !== user.role.toLowerCase()) {
    const pathParts = window.location.pathname.split('/').slice(2); // skip '',':role'
    return <Navigate to={`/${user.role.toLowerCase()}/${pathParts.join('/')}`} replace />;
  }

  return children;
}
export default ProtectedRoute;
