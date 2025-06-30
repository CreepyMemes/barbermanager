import { Navigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';

function ProtectedRoute({ children, role }) {
  const { isAuthenticated, user } = useAuth();

  // Redirect to login if not authenticated
  if (!isAuthenticated) return <Navigate to="/login" replace />;

  // If a role is needed and the user has the wrong role, redirect to their own dashboard
  if (role && user && user.role !== role) {
    const redirectPath = `/${user.role.toLowerCase()}/dashboard`;
    return <Navigate to={redirectPath} replace />;
  }

  return children;
}

export default ProtectedRoute;
