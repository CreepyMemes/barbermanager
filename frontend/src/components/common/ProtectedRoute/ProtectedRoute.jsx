import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) return null; // or show LoadingSpinner, but AuthProvider already does this

  if (!isAuthenticated) {
    return <Navigate to="/" state={{ from: location }} replace />;
  }

  return children;
}
