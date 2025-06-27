import { Navigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';

export default function ProtectedRoute({ children, role }) {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) return null;

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // If role is specified, check user role
  if (role && user?.role !== role) {
    // Optionally redirect to user's "main" page
    const redirectPath = user ? `/${user.role.toLowerCase()}/dashboard` : '/login';
    return <Navigate to={redirectPath} replace />;
  }

  return children;
}
