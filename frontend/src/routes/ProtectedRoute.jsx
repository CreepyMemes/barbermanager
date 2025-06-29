import { Navigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';

function ProtectedRoute({ children, role }) {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) return null;

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // If role is specified, check user role (if user is authenticated, user object should exist)
  if (role && user?.role !== role) {
    const redirectPath = `/${user.role.toLowerCase()}/dashboard`;
    return <Navigate to={redirectPath} replace />;
  }

  return children;
}

export default ProtectedRoute;
